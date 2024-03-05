# ZeroTrustArtifactsRepo

This are the instructions to deploy the Zero Trust application with AWS Verified Access and Amazon VPC Lattice Integration

## Table of Contents

- [Requirements](#installation)
- [Building the Image container](#usage)
- [Contributing](#contributing)
- [License](#license)

## Requirements

1) You need to have a public domain, like: aws.example.com
2) You need to have a public certificate hosted in AWS ACM for the previous domain
3) You need to have the Amazon VPC Lattice part of the code deployed
4) Create the Amazon Route53 private hosted zone for Amazon VPC Lattice service
5) Create an Amazon ECR repository

## Building the Image container

1) Clone the art-container folder to your local environment and open the app/main.py in your favorite code editor
2) In the line 117 of the file, change <https://YourLatticeServiceDomain.com> for your Amazon VPC Lattice service domain
3) Open the command line in the art-container folder and run the following commands to build the docker image and to upload it to the previous created Amazon ECR repository
```bash
docker build --platform=linux/amd64 -t art-container .
docker tag art-container:latest "YourAccountID".dkr.ecr."YourAWSRegion".amazonaws.com/art-container:latest-v2
docker push "YourAccountID".dkr.ecr.YourAWSRegion.amazonaws.com/art-container:latest-v2
```
### Subsection 1

Additional details or subsections under Usage.

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
