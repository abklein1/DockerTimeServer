# Blue/Green Deployment Example

## Infrastructure Overview

We have a Jenkins master running on an Ubuntu 20.04 VirtualBox VM named **"Jhost"**. Jhost runs two declarative pipelines stored in GitHub defined by Jenkinsfiles (**Jenkinsfile**, **Jenkinsfile-BG**). Jenkinsfile runs an official Maven image *maven:3.8.7-eclipse-temurin-17* to build and test the TimeServer within a container. Jenkinsfile-BG is the pipeline responsible for the blue-green deployment and it runs directly on master.

The **TimeServer** is Java-based servlet using the Spring Boot framework. This implementation uses Maven and Apache Tomcat, both are default configurations. TimeServer can be run within a container defined in `TimeServer/Dockerfile` although for the full demonstration the TimeServer is run directly on a VM or EC2 instance.

**TimeTestApp** is a python script that is used to poll TimeServer during the blue/green deployment.

The hosting infrastructure is built within AWS EC2. TimeServer is deployed to two t2.micro instance types. Each instance exists inside their own Target group within EC2 (one instance in **Blue** and one in **Green**). 

Each target group has an associated Listener ARN (Blue: *arn:aws:elasticloadbalancing:us-east-2:283044168142:targetgroup/Blue/28fafd93d214aacb* Green: *arn:aws:elasticloadbalancing:us-east-2:283044168142:targetgroup/Green/4cf40e1547e1c331*). An Application Load Balancer (**BG-load-balancer**: *BG-load-balancer-1671879933.us-east-2.elb.amazonaws.com*) manages both ARNs. The load balancer contains a single ARN on HTTP:8080 (*arn:aws:elasticloadbalancing:us-east-2:283044168142:listener/app/BG-load-balancer/fb5f67b4b97973d0/44f32aec7ee9095a*)

The TimeServer is deployed to each EC2 instance and is run as a `.jar` through a script *start.sh* that is stored locally on each machine. In an ideal situation we would be using ECS/ECR or provisioning these machines with Ansible at the very least, but for this demonstration the machines have been manually configured to run the servlet. "start.sh" runs the jar file using `screen` so that the server will continue to run after the Jenkinsfile completes (and usually kills all child nodes)

