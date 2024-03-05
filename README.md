# ZeroTrustArtifactsRepo

This are the instructions to deploy the Zero Trust application with AWS Verified Access and Amazon VPC Lattice Integration

## Table of Contents

- [Requirements](#requirements)
- [Building the Image container](#building)
- [Deploying the Infrastructure](#deploying)
- [License](#license)

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

### Subsection 2

More information or subsections under Usage.

## Contributing

Guidelines for contributors or how others can contribute to your project.

## License

Information about the license under which your project is distributed.

## Screenshots

![Screenshot 1](/images/screenshot1.png)
Description of the screenshot.

![Screenshot 2](/images/screenshot2.png)
Description of the screenshot.
