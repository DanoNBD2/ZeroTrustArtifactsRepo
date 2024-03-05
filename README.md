# ZeroTrustArtifactsRepo

This are the instructions to deploy the Zero Trust application with AWS Verified Access and Amazon VPC Lattice Integration. Note: This is the first version of the code and you'll need do some manual stuff. The second version will have all of this automated for you.

## Table of Contents

- [Requirements](#requirements)
- [Building the Image container](#building)
- [Deploying the Infrastructure](#deploying)
- [Configure the application](#license)

## Requirements

1) You need to have AWS CLI and AWS account credentials installed in your local environment
2) You need to have a public domain, like: aws.example.com
3) You need to have a public certificate hosted in AWS ACM for the previous domain
4) You need to have the Amazon VPC Lattice part of the code deployed
5) Create the Amazon Route53 private hosted zone for Amazon VPC Lattice service
6) Create an Amazon ECR repository

## Building the Image container

1) Clone the art-container folder to your local environment and open the app/main.py in your favorite code editor
2) In the line 117 of the file, change <https://YourLatticeServiceDomain.com> for your Amazon VPC Lattice service domain
3) Open the command line in the art-container folder and run the following commands to build the docker image and to upload it to the previous created Amazon ECR repository
```bash
docker build --platform=linux/amd64 -t art-container .
docker tag art-container:latest "YourAccountID".dkr.ecr."YourAWSRegion".amazonaws.com/art-container:latest-v2
docker push "YourAccountID".dkr.ecr.YourAWSRegion.amazonaws.com/art-container:latest-v2
```
### Deploying the Infrastructure

Select your desired AWS Region, for example, eu-west-1 (Ireland) and click this button to deploy the AWS Verified access infrastructure 

[![Launch CFN stack](https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png)](https://eu-west-1.console.aws.amazon.com/cloudformation/home?region=eu-west-1#/stacks/quickcreate?templateUrl=https://technical-tracks-march2024.s3.eu-west-1.amazonaws.com/ava-cognito.yaml)

The template takes approximate 25 minutes to deploy.

### Configure the application

1) Go to Amazon EC2 console, select the EC2 instance called "EC2HostingTheAVAWorkload" and connect into it using Sessions Mananger
2) Run the following commands:
```bash
sudo yum update -y
sudo yum install docker -y
sudo service docker start
sudo systemctl enable docker
sudo su -
usermod -aG docker ec2-user
exit
sudo su -
ACCOUNT_ID=$(aws sts get-caller-identity --query "Account" --output text)
REGION=$(curl -s http://169.254.169.254/latest/meta-data/placement/availability-zone | sed 's/.$//')
aws ecr get-login-password --region ${REGION} | docker login --username AWS --password-stdin ${ACCOUNT_ID}.dkr.ecr.${REGION}.amazonaws.com
docker pull ${ACCOUNT_ID}.dkr.ecr.${REGION}.amazonaws.com/art-container:latest-v2
docker run -d --network host --name art-container -p 80:80 -e GREETING="Zero Trust Demo" -e MIRROR_REQ=true -e REGION=${REGION} ${ACCOUNT_ID}.dkr.ecr.eu-west-1.amazonaws.com/art-container:latest-v2
```

## Contributing

Guidelines for contributors or how others can contribute to your project.

## License

Information about the license under which your project is distributed.

## Screenshots

![Screenshot 1](/images/screenshot1.png)
Description of the screenshot.

![Screenshot 2](/images/screenshot2.png)
Description of the screenshot.
