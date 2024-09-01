# Smart Building Distributed Software Architecture (DSA)

## Overview
This repository contains the codebase for the Distributed Software Architecture (DSA) designed for Smart Building (SB) applications, as proposed in the accompanying paper. The DSA is based on the principles of the Reactive Manifesto (RM) and aims to optimize distributed processing, latency, flexibility, security, cost-effectiveness, and scalability within smart building environments.

## Features
- Implementation of the DSA architecture following RM principles.
- Analysis of different deployment configurations, with a focus on container orchestrators.
- Performance testing demonstrating the benefits of using a container orchestrator, including enhanced distributed processing, reduced latency, increased flexibility, improved security, and cost-effectiveness.
- Application of the Design Science Research (DSR) methodology to iteratively develop and refine the DSA artifact.
- Testing procedures emphasizing performance as the primary evaluation metric.
- Integration with Multi-Agent Systems, ontologies, and Federated Learning components to create a comprehensive solution for smart building management.
- Extensive applicability across various IoT domains, including Smart Home setups, Campus environments, City infrastructure, and Health-related applications.

## Requirements
- [Container orchestrator](#) (e.g., Kubernetes)
- [Programming language and frameworks](#) (Go, Javascript)
- [Other dependencies](#) (Cloud provider)



## Usage
Run the microservices on your private network or at your preferred cloud provider.

Migrate and seed the Schema located at api-rest/migration/000001_create_ddl.up.sql at your preferred private/public cloud database.

Kubernetes assets can be found in the config folder.

Load tester tool and scripts can be found in the load-test folder.


## Contribution
We welcome contributions to enhance the functionality, performance, and usability of the DSA codebase. If you're interested in contributing, please follow these guidelines:
- Fork the repository and create a new branch for your feature or bug fix.
- Ensure that your code adheres to the established coding standards and practices.
- Submit a pull request detailing the changes made and any relevant documentation updates.
- Participate in code reviews and discussions to facilitate collaborative development.

## License
MIT License 

## Acknowledgments
This research and development effort were made possible by the contributions of Gustavo Freire, Herminio Paucar e Julio Cezar Estrella and the support of the Laboratory of Distributed Systems and Concurrent Programming (LaSDPC) at São Paulo University.
