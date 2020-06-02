from django.db import models
from kubernetes.client.apis import core_v1_api
from kubernetes  import client, config
from django.contrib.auth.models import User
from django.conf import settings
from kubernetes.client.rest import ApiException
import yaml 
import random
import logging
import os 

def get_kube_config():
    if os.path.isfile('/var/run/secrets/kubernetes.io/serviceaccount/token'):
        return config.load_incluster_config()
    else:
        return config.load_kube_config()
    

class UserService(models.Model):
    name          = models.CharField(max_length=200)
    port          = models.CharField(max_length=5)
    username      = models.ForeignKey(User, on_delete=models.CASCADE)
    password      = models.CharField(max_length=200)
    service       = models.CharField(max_length=10)
    path          = models.CharField(max_length=50)
    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "userService"

class Pynote:
    ## Model to create PyNote
    name = 'Pynote'
    get_kube_config()
    kube = client.ExtensionsV1beta1Api()
    api = core_v1_api.CoreV1Api()

    ## Environment is used for namespace
    environment = getattr(settings, 'ENVIRONMENT', None)
    namespace   = f'{environment}-students'

   
    def available_port(self):
        ## Function will find available port 
        while True:
            random_port = random.choice(list(range(7000, 7100)))
            if not UserService.objects.filter(port=random_port).first():
                return random_port


    def generate_templates(self, username, password, environment, service_path=None):
        ## Function generates all templates <pod>, <service>, <ingress>
        templates = {}
        template_port = self.available_port()
        host = f'{self.environment}.academy.fuchicorp.com'
        ingress_name  = f'{self.environment}-pynote-ingress'
        namespace     = f'{self.environment}-students'

        if service_path is None:
            templates['pynotelink'] = f'/services/pynotes/{username}'
            templates['path'] = {'path': f'/services/pynotes/{username}', 'backend': {'serviceName': username, 'servicePort': template_port}}
        else:
            templates['pynotelink'] = service_path
            templates['path'] = {'path': f'{service_path}', 'backend': {'serviceName': username, 'servicePort': template_port}}
            
        with open('kubernetes/pynote-pod.yaml' ) as file:
            pod = yaml.load(file, Loader=yaml.FullLoader)
            pod['metadata']['name']              = username
            pod['metadata']['labels']['run']     = username
            pod['spec']['containers'][0]['name'] = username
            pod['spec']['containers'][0]['args'] = [ f"--username={username}", f"--password={password}"]

            if service_path is None:
                pod['spec']['containers'][0]['env'].append({"name": "URL_PATH", "value": f'/services/pynotes/{username}'}) 
            else:
                pod['spec']['containers'][0]['env'].append({"name": "URL_PATH", "value": f'{service_path}'}) 

            templates['pod'] = pod

        with open('kubernetes/pynote-service.yaml') as file:
            service = yaml.load(file, Loader=yaml.FullLoader)
            service['metadata']['labels']['run'] = username
            service['spec']['ports'][0]['port']  = template_port
            service['spec']['selector']['run']   = username
            service['metadata']['name']          = username
            templates['service']                 = service

        with open('kubernetes/pynote-ingress.yaml') as file:
            ingress = yaml.load(file, Loader=yaml.FullLoader)
            ingress['spec']['rules'][0]['host']  = host
            ingress['spec']['rules'][0]['http']['paths'].append(templates['path'])
            ingress['metadata']['name']          = ingress_name
            ingress['metadata']['namespace']     = namespace
            templates['ingress']                 = ingress
        return templates

    def existing_ingess(self, ingerssname, namespace):
        list_ingress = self.kube.list_namespaced_ingress(namespace).items
        for item in list_ingress:
            if item.metadata.name == ingerssname:
                return item
        else:
            return False

    def create_service(self, username, password, service_path=None):
        ## Function to create service pynote 
        pynote_name    = username.lower()
        pynote_pass    = password
        ingress_name   = f'{self.environment}-pynote-ingress'
        namespace      = f'{self.environment}-students'

        if service_path is None:
            deployment = self.generate_templates(pynote_name, pynote_pass, self.environment)
        else:
            deployment = self.generate_templates(pynote_name, pynote_pass, self.environment, service_path)
        if not self.is_pod_exist(pynote_name):
            self.api.create_namespaced_pod(body=deployment['pod'], namespace=namespace)
        if not self.is_service_exist(pynote_name):
            self.api.create_namespaced_service(body=deployment['service'], namespace=namespace)
        exist_ingress  = self.existing_ingess(ingress_name, namespace)
        if exist_ingress:
            exist_ingress.spec.rules[0].http.paths.append(deployment['path'])
            self.kube.replace_namespaced_ingress(exist_ingress.metadata.name, namespace, body=exist_ingress)
        else:
            self.kube.create_namespaced_ingress(namespace, body=deployment['ingress'])
        return deployment

    def is_pod_exist(self, username):
        try:
            self.api.read_namespaced_pod(username, self.namespace)
            return True
        except ApiException:
            return False
    
    def is_service_exist(self, username):
        try:
            self.api.read_namespaced_service(username, self.namespace)
            return True
        except ApiException:
            return False
    
    def is_ingress_exist(self):
        try:
            self.kube.read_namespaced_ingress(f"{self.environment}-pynote-ingress", self.namespace)
            return True
        except ApiException:
            return False

    def delete_service(self, username):
        ## Function to delete the service
        pynote_name    = username.lower()
        ingress_name   = f'{self.environment}-pynote-ingress'
        namespace      = f'{self.environment}-students'
        exist_ingress  = self.existing_ingess(ingress_name, namespace)
        try:
            self.api.delete_namespaced_pod(pynote_name, namespace)
            logging.warning(f'Deleted a pod {pynote_name}')
            self.api.delete_namespaced_service(pynote_name, namespace)
            logging.warning(f'Deleted a service {pynote_name}')
        except:
            logging.warning('Trying to delete service and pod was not successed.')
        if exist_ingress:
            if 1 < len(exist_ingress.spec.rules[0].http.paths):
                for i in exist_ingress.spec.rules[0].http.paths:
                    if username in i.path:
                        exist_ingress.spec.rules[0].http.paths.remove(i)
                exist_ingress.metadata.resource_version = ''
                self.kube.patch_namespaced_ingress(exist_ingress.metadata.name, namespace, body=exist_ingress)
            else:
                self.kube.delete_namespaced_ingress(ingress_name, namespace)
        try:

            user = User.objects.get(username=username)
            service = UserService.objects.get(username=user).first()
            service.delete()  
            logging.warning(f"Pynote has been delete for {username}") 
        except Exception as e:
            logging.error(f"Error: {e}")      


class Jenkins:
    name = 'Jenkins'
    pass

class WebShell:
    name = 'WebShell'
    pass

class GoNote:
    name = 'GoNote'
    pass 

def get_service(name):

    if 'pynote' in name.lower():
        return Pynote()

    elif 'jenkins' in name.lower():
        Jenkins()

    elif 'webshell' in name.lower():
        WebShell()

    elif 'webshell' in name.lower():
        GoNote()