serverless_finops_batch = [
  {
    "q": "How do you ensure high availability in a Kubernetes cluster?",
    "topic": "Kubernetes",
    "diff": "Senior",
    "ans": "To ensure HA, run multiple replicas of control plane components across different Availability Zones (AZs). Use a load balancer for the API server. Ensure worker nodes are also spread across AZs.",
    "keys": "Control Plane, Replicas, Availability Zones, Load Balancer"
  },
  {
    "q": "Explain the difference between vertical and horizontal scaling.",
    "topic": "System Design",
    "diff": "Junior",
    "ans": "Vertical scaling (scaling up) means adding more power (CPU/RAM) to an existing machine. Horizontal scaling (scaling out) means adding more machines to the pool to share the load.",
    "keys": "Scaling Up vs Out, CPU/RAM vs Nodes, Distributed Systems"
  },
  {
    "q": "What is the purpose of a VPC peering connection?",
    "topic": "Networking",
    "diff": "Mid",
    "ans": "VPC peering allows two Virtual Private Clouds to communicate with each other as if they are on the same network. It routes traffic using private IP addresses.",
    "keys": "Private IP, Network Routing, Cross-Account Access"
  },
  {
    "q": "What is the difference between a Pod and a Deployment in Kubernetes?",
    "topic": "Kubernetes",
    "diff": "Junior",
    "ans": "A Pod is the smallest deployable unit representing a single instance of a running process. A Deployment is a higher-level abstraction that manages Pods, handling replication, updates, and rollbacks automatically.",
    "keys": "Pod vs Deployment, Abstraction, Replication, Rollbacks"
  },
  {
    "q": "Explain the concept of a Sidecar container.",
    "topic": "Kubernetes",
    "diff": "Mid",
    "ans": "A Sidecar is a secondary container running in the same Pod as the main application container. It helps with auxiliary tasks like logging, monitoring, or proxying network traffic (e.g., Envoy in Istio) without changing the main app code.",
    "keys": "Auxiliary task, Same Pod, Logging agent, Proxy"
  },
  {
    "q": "What is the difference between a Headless Service and a standard ClusterIP Service?",
    "topic": "Kubernetes",
    "diff": "Senior",
    "ans": "A standard ClusterIP assigns a single IP to load balance traffic to pods. A Headless Service (ClusterIP: None) does not assign an IP; instead, it returns the DNS records of all backing pods directly, useful for stateful apps like databases requiring direct peer discovery.",
    "keys": "ClusterIP None, DNS records, StatefulSets, Peer discovery"
  },
  {
    "q": "How does Kubernetes handle Secret management securely?",
    "topic": "Kubernetes",
    "diff": "Mid",
    "ans": "Kubernetes Secrets store sensitive data encoded in base64. For higher security, they should be encrypted at rest (ETCD encryption) and injected into Pods as mounted volumes or environment variables, avoiding hardcoding in images.",
    "keys": "Base64, Encryption at Rest, ETCD, Volume Mount"
  },
  {
    "q": "What is a Taint and Toleration?",
    "topic": "Kubernetes",
    "diff": "Mid",
    "ans": "Taints are applied to Nodes to repel certain Pods. Tolerations are applied to Pods to allow them to schedule on tainted nodes. This ensures specific workloads (like GPU tasks) only run on specific hardware.",
    "keys": "Node Taint, Pod Toleration, Scheduling constraint, Dedicated hardware"
  },
  {
    "q": "Describe the CrashLoopBackOff error and how to debug it.",
    "topic": "Kubernetes",
    "diff": "Junior",
    "ans": "It means a Pod starts, crashes, and Kubelet tries to restart it repeatedly. Debug by checking `kubectl logs`, inspecting `kubectl describe pod` for exit codes (OOMKilled), or checking liveness probe failures.",
    "keys": "Restart loop, kubectl logs, Liveness probe, OOMKilled"
  },
  {
    "q": "What is Ingress in Kubernetes?",
    "topic": "Kubernetes",
    "diff": "Junior",
    "ans": "Ingress is an API object that manages external access to services in a cluster, typically HTTP/HTTPS. It provides load balancing, SSL termination, and name-based virtual hosting.",
    "keys": "External access, HTTP/HTTPS, Load Balancing, SSL Termination"
  },
  {
    "q": "Explain the role of ETCD in a Kubernetes Cluster.",
    "topic": "Kubernetes",
    "diff": "Senior",
    "ans": "ETCD is a consistent and highly-available key-value store used as Kubernetes' backing store for all cluster data. It is the single source of truth; if ETCD is lost, the cluster state is lost.",
    "keys": "Key-value store, Single source of truth, Cluster state, Consistency"
  },
  {
    "q": "What is a StatefulSet used for?",
    "topic": "Kubernetes",
    "diff": "Mid",
    "ans": "StatefulSets manage stateful applications (like Databases) where the order of deployment and unique network identifiers (stable hostnames) matter. Unlike Deployments, pods are created sequentially (0, 1, 2).",
    "keys": "Stateful apps, Stable network ID, Ordered deployment, Persistent storage"
  },
  {
    "q": "How do Liveness and Readiness probes differ?",
    "topic": "Kubernetes",
    "diff": "Junior",
    "ans": "Liveness probes restart a container if it crashes/deadlocks. Readiness probes stop traffic to a container until it is ready to serve requests (e.g., after loading cache).",
    "keys": "Restart vs Traffic stop, Deadlock, Startup latency"
  },
  {
    "q": "What is the difference between S3 Standard and S3 Standard-IA?",
    "topic": "AWS",
    "diff": "Junior",
    "ans": "S3 Standard is for frequently accessed data with low latency. Standard-IA (Infrequent Access) is cheaper for storage but charges a retrieval fee, suitable for backups or older data accessed less than once a month.",
    "keys": "Retrieval fee, Access frequency, Cost optimization"
  },
  {
    "q": "Explain the concept of an Availability Zone (AZ) vs a Region.",
    "topic": "AWS",
    "diff": "Junior",
    "ans": "A Region is a separate geographic area (e.g., us-east-1). An AZ is an isolated location within a Region (a distinct data center) with independent power and cooling. Regions contain multiple AZs to allow for high availability.",
    "keys": "Geographic area, Data Center, Isolation, Fault Tolerance"
  },
  {
    "q": "How does a NAT Gateway differ from an Internet Gateway?",
    "topic": "AWS",
    "diff": "Mid",
    "ans": "An Internet Gateway allows resources in a public subnet to talk to the internet. A NAT Gateway allows resources in a PRIVATE subnet to access the internet (for updates) but prevents the internet from initiating connections to them.",
    "keys": "Public vs Private Subnet, Outbound only, Security"
  },
  {
    "q": "What is the purpose of Route 53?",
    "topic": "AWS",
    "diff": "Junior",
    "ans": "Route 53 is AWS's scalable DNS web service. It translates domain names to IP addresses and handles traffic routing policies like Latency-based, Weighted, or Failover routing.",
    "keys": "DNS, Domain registration, Traffic routing policies, Health checks"
  },
  {
    "q": "Explain the Shared Responsibility Model.",
    "topic": "AWS",
    "diff": "Mid",
    "ans": "It defines who secures what. AWS is responsible for 'Security OF the Cloud' (hardware, datacenters, network infrastructure). The customer is responsible for 'Security IN the Cloud' (data encryption, IAM, patching OS).",
    "keys": "Security OF vs IN, Hardware vs Data, Patching, Encryption"
  },
  {
    "q": "What is the difference between Horizontal and Vertical Scaling?",
    "topic": "Architecture",
    "diff": "Junior",
    "ans": "Vertical scaling (Scaling Up) adds more power (CPU/RAM) to a single instance. Horizontal scaling (Scaling Out) adds more instances/nodes to the pool to distribute the load.",
    "keys": "Resources vs Instances, Monolithic vs Distributed, Downtime risk"
  },
  {
    "q": "How would you design a Multi-Region Active-Active architecture?",
    "topic": "Architecture",
    "diff": "Senior",
    "ans": "Deploy app stacks in two regions. Use DynamoDB Global Tables for data replication. Use Route 53 with Latency-based routing to direct users to the nearest region. Ensure stateless app design.",
    "keys": "Global Tables, Route 53 Latency, Stateless, Replication"
  },
  {
    "q": "What is a Lambda Cold Start and how do you mitigate it?",
    "topic": "AWS",
    "diff": "Mid",
    "ans": "Cold start is the latency when a function is invoked for the first time or after a period of inactivity. Mitigate by using Provisioned Concurrency to keep instances warm or choosing languages with faster startup (Python/Go vs Java).",
    "keys": "Latency, Provisioned Concurrency, Initialization time, Keep-warm"
  },
  {
    "q": "Explain the CAP Theorem.",
    "topic": "Architecture",
    "diff": "Senior",
    "ans": "In a distributed system, you can only have 2 out of 3: Consistency (every read receives most recent write), Availability (every request receives a response), and Partition Tolerance (system continues despite network failures).",
    "keys": "Consistency, Availability, Partition Tolerance, Trade-off"
  },
  {
    "q": "What is CloudFront and when would you use it?",
    "topic": "AWS",
    "diff": "Junior",
    "ans": "CloudFront is a CDN (Content Delivery Network). It caches content (images, videos, static sites) at Edge Locations globally to reduce latency for users geographically distant from the origin server.",
    "keys": "CDN, Edge Locations, Caching, Latency reduction"
  },
  {
    "q": "What is the Terraform State file and why is it important?",
    "topic": "Terraform",
    "diff": "Mid",
    "ans": "The State file (`terraform.tfstate`) maps real-world resources to your configuration. It tracks metadata and dependencies, allowing Terraform to know what to update or destroy without checking the cloud API every time.",
    "keys": "Mapping resources, Metadata, Performance, Locking"
  },
  {
    "q": "How do you handle sensitive data in Terraform?",
    "topic": "Terraform",
    "diff": "Senior",
    "ans": "Never hardcode secrets. Use variables marked as `sensitive=true`, retrieve secrets from a vault (AWS Secrets Manager/HashiCorp Vault) at runtime, or use environment variables. State files should be encrypted remotely.",
    "keys": "No hardcoding, AWS Secrets Manager, Sensitive variable, Encrypted State"
  },
  {
    "q": "What is `terraform plan` vs `terraform apply`?",
    "topic": "Terraform",
    "diff": "Junior",
    "ans": "`plan` performs a dry-run, showing what changes will happen without making them. `apply` actually executes the changes to the infrastructure.",
    "keys": "Dry-run, Execution, Verification, Safety check"
  },
  {
    "q": "What is a Terraform Module?",
    "topic": "Terraform",
    "diff": "Mid",
    "ans": "A module is a container for multiple resources that are used together. It allows you to package and reuse infrastructure code (e.g., a standard VPC setup) across different projects.",
    "keys": "Reusability, Encapsulation, Standard VPC, DRY principle"
  },
  {
    "q": "How do you manage Terraform state in a team environment?",
    "topic": "Terraform",
    "diff": "Mid",
    "ans": "Use a Remote Backend (like S3 with DynamoDB for locking). This ensures everyone shares the same state file and prevents two people from modifying infrastructure simultaneously (State Locking).",
    "keys": "Remote Backend, S3 + DynamoDB, State Locking, Collaboration"
  },
  {
    "q": "What is Drift in Infrastructure as Code?",
    "topic": "Terraform",
    "diff": "Mid",
    "ans": "Drift occurs when the actual infrastructure configuration differs from the code definitions (e.g., someone manually changed a Security Group in the console). Tools like `terraform plan` detect this.",
    "keys": "Manual changes, Configuration mismatch, Detection"
  },
  {
    "q": "Explain the `depends_on` meta-argument.",
    "topic": "Terraform",
    "diff": "Senior",
    "ans": "It explicitly creates a dependency between resources when Terraform cannot automatically infer it. For example, ensuring an S3 bucket policy is only applied after the bucket is created.",
    "keys": "Explicit dependency, Ordering, Inference limitation"
  },
  {
    "q": "What is Immutable Infrastructure?",
    "topic": "DevOps",
    "diff": "Senior",
    "ans": "Servers are never modified after deployment. If you need to update, you replace the entire server with a new one. This prevents configuration drift and makes rollbacks easier.",
    "keys": "Replace vs Update, No drift, Consistent deployments"
  },
  {
    "q": "How do you import existing infrastructure into Terraform?",
    "topic": "Terraform",
    "diff": "Senior",
    "ans": "Use `terraform import [resource_id]`. This adds the resource to the state file. You must then manually write the corresponding HCL configuration to match the state.",
    "keys": "State adoption, Manual config match, Migration"
  },
  {
    "q": "What is the purpose of `terraform fmt` and `terraform validate`?",
    "topic": "Terraform",
    "diff": "Junior",
    "ans": "`fmt` rewrites config files to a canonical format and style. `validate` checks whether the configuration is syntactically valid and internally consistent.",
    "keys": "Formatting, Syntax check, Consistency, Linting"
  },
  {
    "q": "What is the difference between Continuous Delivery and Continuous Deployment?",
    "topic": "DevOps",
    "diff": "Mid",
    "ans": "Continuous Delivery means code is automatically built and tested, but requires manual approval to release to production. Continuous Deployment automates the release to production without any manual intervention.",
    "keys": "Manual approval vs Automated release, Production pipeline"
  },
  {
    "q": "Explain Blue-Green Deployment.",
    "topic": "DevOps",
    "diff": "Mid",
    "ans": "A deployment strategy where two identical environments (Blue and Green) exist. Blue runs the current version. You deploy the new version to Green, test it, and then switch traffic (Load Balancer) from Blue to Green instantly.",
    "keys": "Zero downtime, Traffic switch, Rollback capability, Parallel environments"
  },
  {
    "q": "What is a Canary Deployment?",
    "topic": "DevOps",
    "diff": "Senior",
    "ans": "Rolling out a new version to a small subset of users (e.g., 5%) first. If metrics (errors/latency) are stable, the rollout gradually increases to 100%. If not, it rolls back automatically.",
    "keys": "Subset of users, Risk mitigation, Gradual rollout, Metric monitoring"
  },
  {
    "q": "What is GitOps?",
    "topic": "DevOps",
    "diff": "Senior",
    "ans": "A practice where the Git repository is the 'single source of truth' for infrastructure and applications. Changes are made via Pull Requests, and an operator (like ArgoCD) automatically syncs the cluster to match Git.",
    "keys": "Single source of truth, Pull Requests, ArgoCD, Automatic sync"
  },
  {
    "q": "How do you secure a CI/CD pipeline?",
    "topic": "Security",
    "diff": "Senior",
    "ans": "Scan code for secrets (TruffleHog), use short-lived credentials (OIDC), scan container images for vulnerabilities, and ensure least privilege permissions for the CI runner.",
    "keys": "Secret scanning, Image vulnerability scan, OIDC, Least Privilege"
  },
  {
    "q": "What is a Docker Multi-stage build?",
    "topic": "Docker",
    "diff": "Mid",
    "ans": "A method to reduce image size. You use one stage to build the artifact (with all compilers/dependencies) and copy only the final binary to a second, minimal runtime stage (like Alpine).",
    "keys": "Reduce image size, Build dependencies, Runtime separation, Efficiency"
  },
  {
    "q": "Explain the concept of Idempotency.",
    "topic": "DevOps",
    "diff": "Mid",
    "ans": "An operation is idempotent if running it multiple times produces the same result as running it once. In Ansible/Terraform, this means reapplying a config shouldn't break things or create duplicates.",
    "keys": "Repeatability, Same result, No side effects"
  },
  {
    "q": "What is Jenkins Master vs Agent architecture?",
    "topic": "DevOps",
    "diff": "Junior",
    "ans": "The Master handles scheduling, monitoring, and orchestration. The Agents (Slaves) actually execute the build jobs. This offloads the CPU load from the Master.",
    "keys": "Orchestration vs Execution, Distributed builds, Scalability"
  },
  {
    "q": "How do you optimize a Dockerfile?",
    "topic": "Docker",
    "diff": "Mid",
    "ans": "Use lightweight base images (Alpine), order commands from least to most frequently changed (to use caching), and combine RUN commands to reduce layers.",
    "keys": "Layer caching, Alpine, Command ordering, Reduce layers"
  },
  {
    "q": "What is the role of a Reverse Proxy?",
    "topic": "Networking",
    "diff": "Junior",
    "ans": "It sits in front of servers and forwards client requests to them. It handles load balancing, security (hiding server IP), caching, and SSL encryption.",
    "keys": "Load Balancing, Caching, Security, Hiding Origin"
  },
  {
    "q": "What is the difference between a Security Group and a Network ACL (NACL)?",
    "topic": "Security",
    "diff": "Mid",
    "ans": "Security Groups are stateful (allow inbound = automatically allow outbound) and operate at the instance level. NACLs are stateless (need explicit rules for both directions) and operate at the subnet level.",
    "keys": "Stateful vs Stateless, Instance vs Subnet, Firewall rules"
  },
  {
    "q": "What is the Principle of Least Privilege?",
    "topic": "Security",
    "diff": "Junior",
    "ans": "Granting only the minimum permissions necessary for a user or service to perform its job. For example, an EC2 instance should only have S3 Read access if it doesn't need Write access.",
    "keys": "Minimum permissions, Granular access, IAM policies"
  },
  {
    "q": "Explain SSL/TLS Handshake.",
    "topic": "Security",
    "diff": "Senior",
    "ans": "The process where client and server exchange keys to establish a secure connection. Steps: Client Hello, Server Hello (Certificate), Key Exchange, and Verification.",
    "keys": "Encryption, Certificate, Key Exchange, Secure connection"
  },
  {
    "q": "How do you protect against DDoS attacks in the cloud?",
    "topic": "Security",
    "diff": "Mid",
    "ans": "Use services like AWS Shield or Cloudflare. implement Autoscaling to absorb traffic, use CloudFront (CDN) to cache requests, and configure WAF (Web Application Firewall) to block malicious IPs.",
    "keys": "WAF, AWS Shield, CDN caching, Autoscaling absorption"
  },
  {
    "q": "What is a Bastion Host?",
    "topic": "Security",
    "diff": "Junior",
    "ans": "A special server in a public subnet used as a secure gateway to access private instances (via SSH/RDP). It should have strict IP whitelisting and auditing enabled.",
    "keys": "Jump box, Secure Gateway, Private access, IP whitelisting"
  },
  {
    "q": "What is the 3-tier architecture?",
    "topic": "Architecture",
    "diff": "Junior",
    "ans": "Splitting an app into Presentation Tier (Web/UI), Application Tier (Logic/API), and Data Tier (Database). Each tier can be scaled and secured independently (e.g., DB in private subnet).",
    "keys": "Presentation/App/Data, Decoupling, Security zones, Scalability"
  },
  {
    "q": "What is CIDR notation?",
    "topic": "Networking",
    "diff": "Junior",
    "ans": "A method to define IP address ranges. /32 is one IP, /24 is 256 IPs. A lower number means a larger network.",
    "keys": "IP Range, Subnet mask, Network size"
  },
  {
    "q": "How does DNS Load Balancing work?",
    "topic": "Networking",
    "diff": "Mid",
    "ans": "DNS returns multiple IP addresses for a single domain, or different IPs based on the user's location. The browser tries one of the IPs, distributing traffic before it even hits the network load balancer.",
    "keys": "Traffic distribution, Client-side balancing, A-Records"
  },
  {
    "q": "What is a VPN vs Direct Connect?",
    "topic": "Networking",
    "diff": "Senior",
    "ans": "VPN connects your office to the cloud over the public internet (encrypted but variable latency). Direct Connect is a dedicated physical fiber link offering consistent low latency and high bandwidth.",
    "keys": "Public Internet vs Dedicated Fiber, Latency, Bandwidth"
  },
  {
    "q": "What is Cross-Origin Resource Sharing (CORS)?",
    "topic": "Web",
    "diff": "Mid",
    "ans": "A browser security feature that restricts web pages from making requests to a different domain than the one that served the page. You must configure headers to explicitly allow this.",
    "keys": "Browser security, Domain restriction, Headers, API access"
  },
  {
    "q": "You have a Pod in 'Pending' state for 30 minutes. How do you troubleshoot this?",
    "topic": "Kubernetes Troubleshooting",
    "diff": "Senior",
    "ans": "Check `kubectl describe pod` for events. Common causes: insufficient CPU/Memory resources (Cluster Autoscaler needed), Taint/Toleration mismatch, or PVC binding issues (StorageClass missing).",
    "keys": "Pending state, Resource limits, Cluster Autoscaler, PVC binding, Taints"
  },
  {
    "q": "Explain the OOMKilled error. How do you fix it without just increasing memory blindly?",
    "topic": "Kubernetes Troubleshooting",
    "diff": "Senior",
    "ans": "OOMKilled means the container used more RAM than its 'Limit'. Fix by profiling the app to find memory leaks. If the app is Java, check JVM heap settings. Only increase limits if the workload genuinely requires it.",
    "keys": "OOMKilled, Memory Limit, Profiling, Memory Leak, JVM Heap"
  },
  {
    "q": "How does Kubernetes Horizontal Pod Autoscaler (HPA) work?",
    "topic": "Kubernetes Architecture",
    "diff": "Mid",
    "ans": "HPA monitors metrics (like CPU utilization or custom Prometheus metrics) via the Metrics Server. It calculates the desired number of replicas to meet the target usage (e.g., 50% CPU) and scales the Deployment up or down.",
    "keys": "Metrics Server, CPU utilization, Desired replicas, Scale up/down"
  },
  {
    "q": "What is the difference between a DaemonSet and a ReplicaSet?",
    "topic": "Kubernetes Architecture",
    "diff": "Mid",
    "ans": "A ReplicaSet ensures a specific number of pods run across the cluster (e.g., 3 web servers). A DaemonSet ensures EXACTLY ONE pod runs on EVERY node (e.g., log collectors like Fluentd or monitoring agents).",
    "keys": "One per node, Log collector, Monitoring agent, Cluster-wide"
  },
  {
    "q": "Explain Blue/Green Deployment strategy in Kubernetes.",
    "topic": "Kubernetes Deployment",
    "diff": "Senior",
    "ans": "Create a new Deployment (Green) alongside the old one (Blue). Wait for Green to pass health checks. Switch the Service's selector to point to Green's labels. If issues arise, switch back to Blue instantly.",
    "keys": "Service Selector, Label switching, Zero downtime, Instant rollback"
  },
  {
    "q": "What is a Service Mesh (e.g., Istio) and why would you use it?",
    "topic": "Kubernetes Advanced",
    "diff": "Senior",
    "ans": "A Service Mesh manages traffic between services (East-West traffic). It provides mTLS security, detailed observability (tracing), and advanced traffic control (canary splits, retries, circuit breaking) without changing application code.",
    "keys": "mTLS, Observability, Traffic splitting, Circuit breaking, Sidecar"
  },
  {
    "q": "How do you upgrade a Kubernetes cluster with zero downtime?",
    "topic": "Kubernetes Operations",
    "diff": "Senior",
    "ans": "Upgrade the Control Plane first. Then, drain worker nodes one by one (`kubectl drain`). This evicts pods to other nodes. Upgrade the node's Kubelet/OS, then uncordon it. Repeat for all nodes.",
    "keys": "Control Plane first, Drain nodes, Eviction, Rolling upgrade"
  },
  {
    "q": "What is Network Policy in Kubernetes?",
    "topic": "Kubernetes Security",
    "diff": "Mid",
    "ans": "It acts like a firewall for pods. By default, all pods can talk to each other. Network Policies allow you to whitelist traffic, e.g., 'Only the Frontend Pods can talk to the Backend Database Pods'.",
    "keys": "Pod Firewall, Whitelist, Ingress/Egress rules, Deny by default"
  },
  {
    "q": "Explain the concept of 'GitOps' using ArgoCD.",
    "topic": "DevOps",
    "diff": "Mid",
    "ans": "GitOps uses a Git repository as the single source of truth for infrastructure. ArgoCD (running inside K8s) watches the Git repo. If YAML changes in Git, ArgoCD automatically syncs the live cluster to match the new state.",
    "keys": "Single source of truth, Pull-based sync, Drift detection, ArgoCD"
  },
  {
    "q": "What is a PV (Persistent Volume) and PVC (Claim)?",
    "topic": "Kubernetes Storage",
    "diff": "Junior",
    "ans": "PV is the physical storage resource (e.g., an EBS drive) provisioned by admin. PVC is a request for storage by a user/pod. Kubernetes binds the PVC to a matching PV so the Pod can use it.",
    "keys": "Storage abstraction, Request vs Resource, Binding, Data persistence"
  },
  {
    "q": "You need to store sensitive credit card data. How do you design this on AWS?",
    "topic": "Cloud Security",
    "diff": "Senior",
    "ans": "Store data in a dedicated Private Subnet or separate VPC. Use AWS KMS for encryption at rest. Use Tokenization (replace card numbers with tokens). Enable Macie to discover sensitive data. Ensure S3 buckets block public access.",
    "keys": "KMS, Encryption, Private Subnet, Tokenization, Macie, Compliance"
  },
  {
    "q": "Your website is suffering from a DDoS attack. What immediate steps do you take?",
    "topic": "Cloud Security",
    "diff": "Senior",
    "ans": "Enable AWS Shield Advanced. Config AWS WAF to block malicious IPs or Geo-block countries. Verify CloudFront caching is absorbing hits. Scale ASG (Auto Scaling Group) out to handle load.",
    "keys": "Shield Advanced, WAF rules, CloudFront, Geo-blocking, Scaling"
  },
  {
    "q": "Difference between SQS (Simple Queue Service) and SNS (Simple Notification Service).",
    "topic": "AWS Architecture",
    "diff": "Mid",
    "ans": "SQS is a Queue (pull-based): one consumer polls and processes a message. SNS is a Pub/Sub topic (push-based): one message is instantly pushed to many subscribers (Email, Lambda, SQS).",
    "keys": "Pull vs Push, Queue vs Topic, One-to-one vs One-to-many"
  },
  {
    "q": "How do you design a serverless API that handles 1 million requests per minute?",
    "topic": "Serverless",
    "diff": "Senior",
    "ans": "Use API Gateway (with caching/throttling) -> Lambda (increase concurrency limits) -> DynamoDB (On-Demand mode). Use SQS to buffer writes if DB is overwhelmed.",
    "keys": "API Gateway Caching, Lambda Concurrency, DynamoDB On-Demand, SQS buffering"
  },
  {
    "q": "What is AWS Transit Gateway?",
    "topic": "AWS Networking",
    "diff": "Senior",
    "ans": "It acts as a cloud router to connect hundreds of VPCs and on-premise networks (VPN/Direct Connect) in a hub-and-spoke topology, simplifying peering complexity.",
    "keys": "Hub-and-spoke, VPC peering alternative, Centralized routing"
  },
  {
    "q": "Explain 'Fan-out' architecture pattern.",
    "topic": "Architecture Patterns",
    "diff": "Senior",
    "ans": "Using SNS to send a single message to multiple SQS queues in parallel. This allows different microservices to process the same event asynchronously (e.g., one queue for 'Email User', one for 'Audit Log').",
    "keys": "SNS to SQS, Parallel processing, Decoupling, Asynchronous"
  },
  {
    "q": "When would you use DynamoDB vs RDS?",
    "topic": "Database",
    "diff": "Mid",
    "ans": "Use RDS (SQL) for relational data, complex joins, and transactions (ACID). Use DynamoDB (NoSQL) for massive scale, simple key-value lookups, and flexible schemas (e.g., user sessions, gaming leaderboards).",
    "keys": "Relational vs NoSQL, Joins vs Key-Value, ACID vs Scale"
  },
  {
    "q": "What is VPC Endpoints (PrivateLink)?",
    "topic": "AWS Networking",
    "diff": "Mid",
    "ans": "They allow instances in a private subnet to connect to AWS services (like S3 or DynamoDB) privately without going over the public internet or using a NAT Gateway.",
    "keys": "Private access, Security, No Internet Gateway, Cost saving"
  },
  {
    "q": "Explain the Strangler Fig pattern for migration.",
    "topic": "Architecture Patterns",
    "diff": "Senior",
    "ans": "Gradually migrate a monolithic app to microservices by replacing functionality piece by piece. Put a proxy (API Gateway) in front; route new features to microservices and legacy traffic to the monolith until the monolith is gone.",
    "keys": "Incremental migration, API Gateway proxy, Monolith decomposition"
  },
  {
    "q": "How does AWS Spot Instance work and when to use it?",
    "topic": "AWS Cost Optimization",
    "diff": "Junior",
    "ans": "Spot instances are unused EC2 capacity offered at up to 90% discount. They can be interrupted with 2 minutes notice. Use them for fault-tolerant, stateless workloads like batch processing or CI/CD agents.",
    "keys": "Cost saving, Interruption risk, Stateless workloads, Batch jobs"
  },
  {
    "q": "What is Database Sharding?",
    "topic": "Database Architecture",
    "diff": "Senior",
    "ans": "Splitting a large database into smaller, faster, easily managed parts called shards (usually based on a partition key like UserID). This allows horizontal scaling of writes.",
    "keys": "Horizontal scaling, Partition key, Write throughput, Complexity"
  },
  {
    "q": "How do you secure an S3 bucket?",
    "topic": "AWS Security",
    "diff": "Mid",
    "ans": "Block Public Access setting. Use Bucket Policies for fine-grained permissions. Enable Server-Side Encryption (SSE-S3 or KMS). Enable Versioning (protection against accidental deletes). Use MFA Delete.",
    "keys": "Block Public Access, Bucket Policy, Encryption, Versioning, MFA Delete"
  },
  {
    "q": "What is Chaos Engineering?",
    "topic": "SRE/DevOps",
    "diff": "Senior",
    "ans": "The practice of intentionally introducing failure (killing pods, adding latency) into a system to test its resilience and verify that recovery mechanisms (like autoscaling/failover) work.",
    "keys": "Intentional failure, Resilience testing, Recovery verification"
  },
  {
    "q": "Explain how you would reduce AWS costs for a startup.",
    "topic": "Cost Optimization",
    "diff": "Mid",
    "ans": "Right-size EC2 instances. Buy Savings Plans or Reserved Instances for steady workloads. Use Spot Instances for batch jobs. Set S3 Lifecycle rules to move old data to Glacier. Delete unattached EBS volumes.",
    "keys": "Right-sizing, Reserved Instances, Spot, Lifecycle rules, Waste removal"
  },
  {
    "q": "What is a Multi-AZ RDS deployment?",
    "topic": "Database",
    "diff": "Mid",
    "ans": "A primary DB instance replicates data synchronously to a standby instance in a different AZ. If the primary fails, AWS automatically fails over to the standby. This is for High Availability, NOT scaling read performance.",
    "keys": "Synchronous replication, High Availability, Automatic failover, Not for scaling"
  },
  {
    "q": "How do you handle Terraform State locking errors?",
    "topic": "Terraform Troubleshooting",
    "diff": "Mid",
    "ans": "If a `terraform apply` crashes, the lock remains in DynamoDB. Verify no one else is running it, then use `terraform force-unlock [LockID]` to release it manually.",
    "keys": "DynamoDB lock, force-unlock, Crash recovery"
  },
  {
    "q": "What is 'Immutable Infrastructure' vs 'Configuration Management' (Ansible)?",
    "topic": "DevOps Theory",
    "diff": "Mid",
    "ans": "Immutable (Terraform/Packer) means you replace the whole server for an update. Config Management (Ansible/Chef) means you patch/update the existing server in place. Immutable is preferred for cloud stability.",
    "keys": "Replace vs Patch, Drift avoidance, Stability, Packer"
  },
  {
    "q": "Explain Terraform Workspaces.",
    "topic": "Terraform",
    "diff": "Mid",
    "ans": "Workspaces allow you to use the same HCL code to manage multiple environments (dev, stage, prod) with separate state files. However, separating by directory structure is often safer for production isolation.",
    "keys": "Multiple environments, Separate states, Directory isolation preferred"
  },
  {
    "q": "How do you use `terraform import`?",
    "topic": "Terraform",
    "diff": "Senior",
    "ans": "It brings resources created manually (via console) into Terraform management. Run `terraform import aws_instance.myvm i-12345`. You must then write the HCL code to match the imported state.",
    "keys": "Legacy adoption, Manual sync, State update"
  },
  {
    "q": "What is the 'Count' vs 'For_Each' loop in Terraform?",
    "topic": "Terraform Advanced",
    "diff": "Senior",
    "ans": "`count` is simple but uses index (0, 1, 2); if you delete item 1, item 2 shifts, causing recreation. `for_each` uses keys (map/set), which is stable and safer for managing lists of resources like users or subnets.",
    "keys": "Index vs Key, Stability, Resource shifting, Lists vs Maps"
  },
  {
    "q": "How do you test your Infrastructure as Code?",
    "topic": "DevOps Testing",
    "diff": "Senior",
    "ans": "Use `terraform validate` for syntax. Use `tflint` for best practices. Use `Terratest` (Go library) to spin up real resources, validate them (e.g., check HTTP 200), and destroy them.",
    "keys": "Validation, Linting, Integration testing, Terratest"
  },
  {
    "q": "What is a Self-Hosted Runner in Github Actions?",
    "topic": "CI/CD",
    "diff": "Mid",
    "ans": "A machine you manage that runs CI/CD jobs. Used for security (accessing private resources in VPC) or performance (custom hardware/caching) instead of using Github's public shared runners.",
    "keys": "Private VPC access, Security, Custom hardware, Performance"
  },
  {
    "q": "Explain the concept of 'Artifacts' in a CI/CD pipeline.",
    "topic": "CI/CD",
    "diff": "Junior",
    "ans": "Artifacts are the output of a build stage (JAR file, Docker image, Binary). They are stored in a repository (Artifactory, ECR, Nexus) and passed to the deployment stage. You build once, deploy anywhere.",
    "keys": "Build output, Docker Image, Immutable, Build once deploy anywhere"
  },
  {
    "q": "How do you upgrade a production database using Terraform?",
    "topic": "Terraform Operations",
    "diff": "Senior",
    "ans": "Be careful. Some changes force a resource replacement (destroy/create), causing data loss. Always check `terraform plan`. For DB engines, use `prevent_destroy` lifecycle rule or perform manual snapshots before applying.",
    "keys": "Data loss risk, prevent_destroy, Snapshots, Plan verification"
  },
  {
    "q": "What is 'Dependency Hell' in microservices?",
    "topic": "Microservices",
    "diff": "Mid",
    "ans": "When service A depends on Service B v1.0, but Service C needs Service B v2.0. In microservices, we solve this by containerization (each service brings its own libs) or strict API versioning.",
    "keys": "Versioning conflict, Container isolation, API versioning"
  },
  {
    "q": "How do you check if a port is open on a remote Linux server?",
    "topic": "Linux/Networking",
    "diff": "Junior",
    "ans": "Use `telnet IP PORT`, `nc -zv IP PORT` (Netcat), or `curl -v telnet://IP:PORT`. `ping` only checks ICMP, not specific ports.",
    "keys": "Netcat, Telnet, Connectivity check, ICMP vs TCP"
  },
  {
    "q": "What is the difference between TCP and UDP?",
    "topic": "Networking",
    "diff": "Junior",
    "ans": "TCP is connection-oriented, reliable, and ensures order (e.g., Web, Email). UDP is connectionless, faster, but allows packet loss (e.g., Video streaming, DNS, VoIP).",
    "keys": "Reliable vs Fast, Handshake vs Fire-and-forget, Packet loss"
  },
  {
    "q": "Explain the Linux load average (output of `uptime`).",
    "topic": "Linux",
    "diff": "Mid",
    "ans": "It shows the average number of processes waiting for CPU over 1, 5, and 15 minutes. A load of 1.0 on a single-core CPU means 100% utilization. On a quad-core, 1.0 is only 25% utilization.",
    "keys": "CPU queue, Core count, Utilization metric, 1/5/15 min"
  },
  {
    "q": "How do you find a large file consuming disk space on Linux?",
    "topic": "Linux",
    "diff": "Junior",
    "ans": "Use `du -h --max-depth=1 / | sort -hr` to find large directories. Or `find / -type f -size +100M` to find specific large files.",
    "keys": "du, find command, Disk usage analysis"
  },
  {
    "q": "What is an Inode in Linux?",
    "topic": "Linux Internals",
    "diff": "Senior",
    "ans": "An Inode stores metadata about a file (permissions, owner, size, location blocks) but NOT the filename or data. If you run out of Inodes (lots of tiny files), you can't create new files even if disk space exists.",
    "keys": "Metadata, File limit, Tiny files problem, Disk full error"
  },
  {
    "q": "What does `chmod 755` mean?",
    "topic": "Linux",
    "diff": "Junior",
    "ans": "7 = Read(4)+Write(2)+Execute(1) for Owner. 5 = Read(4)+Execute(1) for Group. 5 = Read(4)+Execute(1) for Others. Standard permission for scripts.",
    "keys": "Permissions, Octal notation, Read/Write/Execute"
  },
  {
    "q": "How do you trace a slow network request?",
    "topic": "Networking Troubleshooting",
    "diff": "Senior",
    "ans": "Use `traceroute` to see hops. Use `tcpdump` or `Wireshark` to inspect packets. Use `dig` to debug DNS resolution time. Use `curl -w` to see time-to-first-byte.",
    "keys": "traceroute, tcpdump, DNS debug, Latency analysis"
  },
  {
    "q": "What is a Zombie Process?",
    "topic": "Linux Internals",
    "diff": "Mid",
    "ans": "A process that has finished execution but its parent hasn't read its exit status yet. It takes up a PID but no CPU/RAM. Too many zombies can fill the process table.",
    "keys": "Defunct, PID exhaustion, Parent process wait"
  },
  {
    "q": "What is a 'Hard Link' vs 'Soft Link' (Symlink)?",
    "topic": "Linux",
    "diff": "Mid",
    "ans": "A Soft Link is a pointer to a filename (like a Windows shortcut); if original is deleted, link breaks. A Hard Link points to the same Inode; deleting the original doesn't delete the data until all hard links are gone.",
    "keys": "Inode pointer vs File pointer, Shortcut, Deletion behavior"
  },
  {
    "q": "Explain the difference between Process and Thread.",
    "topic": "CS Fundamentals",
    "diff": "Mid",
    "ans": "A Process is an independent execution unit with its own memory space. A Thread is a lightweight unit within a process that shares memory with other threads. Threads are faster to create but harder to sync (race conditions).",
    "keys": "Memory isolation vs Shared memory, Heavy vs Light, Concurrency"
  },
  {
    "q": "A server is running out of Inodes, but disk space is 50% free. What happened?",
    "topic": "Linux Troubleshooting",
    "diff": "Senior",
    "ans": "The server has too many small files (e.g., a session cache or mail queue) that consumed all available Inode pointers. Delete these files to free up Inodes, as having free disk space doesn't matter if you have no Inodes left.",
    "keys": "Inodes, Small files, Disk usage, File pointers"
  },
  {
    "q": "How do you check which process is listening on port 8080?",
    "topic": "Linux Networking",
    "diff": "Junior",
    "ans": "Use `netstat -tulpn | grep 8080` or `lsof -i :8080` or `ss -lptn 'sport = :8080'`. This will show the PID and process name using that port.",
    "keys": "netstat, lsof, ss, Port conflict"
  },
  {
    "q": "What is the 'Load Average' in Linux and how is it calculated?",
    "topic": "Linux Performance",
    "diff": "Mid",
    "ans": "It is the average number of processes in the run-queue (CPU) or waiting for disk I/O over 1, 5, and 15 minutes. A load of 4.0 on a 4-core system is 100% utilization. If it's higher, processes are waiting.",
    "keys": "Run-queue, Disk I/O wait, CPU cores, Uptime"
  },
  {
    "q": "A process can't be killed with `kill -9`. What state is it in?",
    "topic": "Linux Internals",
    "diff": "Senior",
    "ans": "It is likely in a 'Uninterruptible Sleep' (D state), often waiting for I/O (like a network mount or bad hard drive). The kernel protects it to prevent data corruption. You usually have to reboot or fix the hardware issue.",
    "keys": "Zombie vs Uninterruptible, D state, I/O wait, Kernel protection"
  },
  {
    "q": "How do you recover a root password if you've lost it?",
    "topic": "Linux Admin",
    "diff": "Mid",
    "ans": "Reboot the server into Single User Mode (edit GRUB, append `init=/bin/bash` or `single`). Remount the root filesystem as read-write (`mount -o remount,rw /`), then run `passwd root`.",
    "keys": "Single User Mode, GRUB, Remount RW, Password reset"
  },
  {
    "q": "Explain the boot process of Linux (High level).",
    "topic": "Linux Internals",
    "diff": "Mid",
    "ans": "BIOS/UEFI -> MBR/GPT -> GRUB (Bootloader) -> Kernel -> Init (Systemd/SysVinit) -> Runlevel/Targets (Userspace).",
    "keys": "BIOS, GRUB, Kernel, Systemd, Init"
  },
  {
    "q": "What is the difference between `hard` and `soft` limits in `ulimit`?",
    "topic": "Linux Security",
    "diff": "Mid",
    "ans": "A Soft limit is a warning threshold that can be increased by the user (up to the hard limit). A Hard limit is the absolute ceiling set by the admin (root) that cannot be exceeded.",
    "keys": "Resource limits, File descriptors, User vs Admin"
  },
  {
    "q": "How do you troubleshoot high I/O wait time?",
    "topic": "Linux Performance",
    "diff": "Senior",
    "ans": "Use `iotop` to identify which process is writing/reading heavily. Use `iostat` to check disk latency. Check `dmesg` for hardware errors. It could be a database doing full table scans or a failing disk.",
    "keys": "iotop, iostat, Disk latency, Hardware failure"
  },
  {
    "q": "What is a 'Zombie Process'?",
    "topic": "Linux Internals",
    "diff": "Junior",
    "ans": "A process that has completed execution but still has an entry in the process table because its parent process hasn't read its exit code (hasn't called `wait()`).",
    "keys": "Defunct, Parent process, Exit code, Process table"
  },
  {
    "q": "How do you persist an environment variable across reboots?",
    "topic": "Linux Admin",
    "diff": "Junior",
    "ans": "Add the export command (e.g., `export JAVA_HOME=...`) to `~/.bashrc` (for user) or `/etc/environment` (system-wide).",
    "keys": ".bashrc, /etc/environment, Profile, Persistence"
  },
  {
    "q": "What is `cron` and how do you edit it?",
    "topic": "Linux Admin",
    "diff": "Junior",
    "ans": "`cron` is a time-based job scheduler. Use `crontab -e` to edit the user's cron table. Syntax: `Minute Hour Day Month Weekday Command`.",
    "keys": "Scheduler, crontab -e, Automation, Syntax"
  },
  {
    "q": "What is the difference between `TCP` and `UDP`?",
    "topic": "Networking",
    "diff": "Junior",
    "ans": "TCP is connection-oriented, reliable, and guarantees order (3-way handshake). UDP is connectionless, faster, but does not guarantee delivery (Fire and forget).",
    "keys": "Reliable vs Fast, Handshake, Packet loss, Streaming"
  },
  {
    "q": "Explain `chmod 777` vs `chmod 755`.",
    "topic": "Linux Security",
    "diff": "Junior",
    "ans": "777 gives Read/Write/Execute to Everyone (Dangerous). 755 gives RWX to Owner, but only Read/Execute to Group and Others (Standard for scripts/directories).",
    "keys": "Permissions, Octal, Security risk, Owner/Group/Other"
  },
  {
    "q": "How do you check the kernel version?",
    "topic": "Linux Admin",
    "diff": "Junior",
    "ans": "Run `uname -r` or `cat /proc/version`.",
    "keys": "uname, /proc/version, Kernel info"
  },
  {
    "q": "What is `swap` memory?",
    "topic": "Linux Performance",
    "diff": "Mid",
    "ans": "It is space on the hard drive used as 'virtual RAM' when physical RAM is full. Relying on swap slows down the system significantly (Thrashing).",
    "keys": "Virtual RAM, Disk paging, Performance penalty, OOM"
  },
  {
    "q": "In Python, how do you handle exceptions properly?",
    "topic": "Python Scripting",
    "diff": "Junior",
    "ans": "Use `try`, `except`, and `finally` blocks. Catch specific exceptions (e.g., `FileNotFoundError`) rather than a bare `except:`. Use `finally` to close resources like file handles.",
    "keys": "try/except/finally, Specific exceptions, Resource cleanup"
  },
  {
    "q": "How do you run a shell command from inside a Python script?",
    "topic": "Python Scripting",
    "diff": "Mid",
    "ans": "Use the `subprocess` module. `subprocess.run(['ls', '-l'], capture_output=True)` is the modern, secure way. Avoid `os.system` as it is less secure and harder to capture output.",
    "keys": "subprocess module, os.system, Security, Output capture"
  },
  {
    "q": "What is a Python Virtual Environment and why use it?",
    "topic": "Python Scripting",
    "diff": "Mid",
    "ans": "It creates an isolated environment for a project with its own dependencies. This prevents version conflicts (e.g., Project A needs boto3 v1.0, Project B needs boto3 v2.0) on the same machine.",
    "keys": "Dependency isolation, venv, pip, Version conflicts"
  },
  {
    "q": "How do you parse a JSON file in Bash?",
    "topic": "Bash Scripting",
    "diff": "Mid",
    "ans": "Bash cannot handle JSON natively well. Use the `jq` tool. Example: `cat file.json | jq '.key'`.",
    "keys": "jq tool, JSON parsing, Native limitation"
  },
  {
    "q": "What does `set -e` do in a Bash script?",
    "topic": "Bash Scripting",
    "diff": "Mid",
    "ans": "It causes the script to exit immediately if any command returns a non-zero status (error). This prevents the script from snowballing errors (e.g., deploying to a server that failed to build).",
    "keys": "Exit on error, Fail fast, Safety, Debugging"
  },
  {
    "q": "Difference between `list` and `tuple` in Python?",
    "topic": "Python Scripting",
    "diff": "Junior",
    "ans": "Lists `[]` are mutable (can change contents). Tuples `()` are immutable (cannot change after creation). Tuples are faster and safer for fixed data.",
    "keys": "Mutable vs Immutable, Performance, Syntax"
  },
  {
    "q": "How would you automate deleting logs older than 7 days?",
    "topic": "Bash Scripting",
    "diff": "Mid",
    "ans": "In Bash: `find /var/log -name '*.log' -mtime +7 -delete`. In Python: Use `os.walk` and `os.path.getmtime`.",
    "keys": "find command, mtime, Retention policy, Automation"
  },
  {
    "q": "What is the `boto3` library?",
    "topic": "Python Scripting",
    "diff": "Junior",
    "ans": "It is the AWS SDK for Python. It allows Python scripts to create, configure, and manage AWS services (like uploading to S3 or starting EC2 instances).",
    "keys": "AWS SDK, Automation, API interaction"
  },
  {
    "q": "Explain `if __name__ == '__main__':` in Python.",
    "topic": "Python Scripting",
    "diff": "Junior",
    "ans": "It checks if the script is being run directly or imported as a module. Code inside this block only runs if the script is the main entry point, not if it's imported by another script.",
    "keys": "Entry point, Module import, Script execution"
  },
  {
    "q": "How do you debug a Bash script?",
    "topic": "Bash Scripting",
    "diff": "Junior",
    "ans": "Run the script with `bash -x script.sh` to print every command before executing it. Or add `set -x` inside the script.",
    "keys": "set -x, Verbose mode, Tracing"
  },
  {
    "q": "How do you read arguments passed to a Bash script?",
    "topic": "Bash Scripting",
    "diff": "Junior",
    "ans": "Use `$1`, `$2` for the first and second arguments. `$@` represents all arguments. `$#` is the count of arguments.",
    "keys": "Positional parameters, $@, $#, Input handling"
  },
  {
    "q": "What is a `generator` in Python?",
    "topic": "Python Scripting",
    "diff": "Senior",
    "ans": "A function that returns an iterator using the `yield` keyword. It generates values one at a time (lazy evaluation) instead of storing them all in memory, which is efficient for large datasets.",
    "keys": "yield, Lazy evaluation, Memory efficiency, Iterator"
  },
  {
    "q": "How do you check if a file exists in Bash?",
    "topic": "Bash Scripting",
    "diff": "Junior",
    "ans": "Use `if [ -f \"/path/to/file\" ]; then ... fi`. Use `-d` for directories.",
    "keys": "File test operators, -f, -d, Conditionals"
  },
  {
    "q": "What is `pip`?",
    "topic": "Python Scripting",
    "diff": "Junior",
    "ans": "The package installer for Python. It connects to PyPI (Python Package Index) to install libraries like `requests`, `flask`, or `boto3`.",
    "keys": "Package manager, PyPI, Dependency management"
  },
  {
    "q": "How do you run tasks in parallel in Bash?",
    "topic": "Bash Scripting",
    "diff": "Mid",
    "ans": "Put the command in the background with `&` and then use `wait` to pause the script until all background jobs finish. Example: `task1 & task2 & wait`.",
    "keys": "Background jobs, Ampersand, wait command, Concurrency"
  },
  {
    "q": "Design a highly available database architecture on AWS.",
    "topic": "System Design",
    "diff": "Senior",
    "ans": "Use Amazon Aurora or RDS Multi-AZ. The primary writes replicate synchronously to a standby in a different AZ. Add Read Replicas for scaling read traffic. Enable automated backups to S3.",
    "keys": "Multi-AZ, Synchronous replication, Read Replicas, Aurora"
  },
  {
    "q": "What is the difference between RPO and RTO?",
    "topic": "Disaster Recovery",
    "diff": "Senior",
    "ans": "RPO (Recovery Point Objective): How much data you can afford to lose (measured in time, e.g., '15 minutes of data'). RTO (Recovery Time Objective): How fast you must be back online after a disaster (e.g., '4 hours').",
    "keys": "Data loss tolerance, Downtime tolerance, Disaster Recovery metrics"
  },
  {
    "q": "How do you handle 'Thundering Herd' problem?",
    "topic": "System Design",
    "diff": "Senior",
    "ans": "This happens when many clients retry a failed request simultaneously, overwhelming the system. Solution: Implement 'Exponential Backoff' with 'Jitter' (randomized delay) in the client retry logic.",
    "keys": "Exponential Backoff, Jitter, Retry logic, Overload"
  },
  {
    "q": "What is a 'Circuit Breaker' pattern?",
    "topic": "Microservices",
    "diff": "Senior",
    "ans": "A design pattern that detects failures in a service calls. If failures cross a threshold, the 'circuit opens' and immediately fails subsequent calls without waiting for timeouts, preventing cascading failures.",
    "keys": "Fail fast, Cascading failure prevention, Resilience"
  },
  {
    "q": "Explain 'Eventual Consistency' vs 'Strong Consistency'.",
    "topic": "System Design",
    "diff": "Mid",
    "ans": "Strong: Reads return the most recent write immediately (e.g., SQL). Eventual: Reads might return stale data for a short time while replicas sync (e.g., DNS, DynamoDB). Eventual offers higher availability.",
    "keys": "CAP Theorem, Replication lag, Availability trade-off"
  },
  {
    "q": "How do you secure secrets in a microservices architecture?",
    "topic": "Security Design",
    "diff": "Senior",
    "ans": "Never store secrets in code/git. Use a centralized secret manager like HashiCorp Vault or AWS Secrets Manager. Inject them into containers as environment variables or mounted volumes at runtime.",
    "keys": "Vault, Secrets Manager, Runtime injection, No hardcoding"
  },
  {
    "q": "What is the 12-Factor App methodology?",
    "topic": "DevOps Theory",
    "diff": "Senior",
    "ans": "A set of best practices for building cloud-native apps. Key factors: Codebase (Git), Dependencies (Explicit), Config (Env vars), Backing Services (Attached resources), Disposability (Fast startup/shutdown).",
    "keys": "Cloud-native standard, Config in Env, Disposability"
  },
  {
    "q": "Design a system to handle millions of webhooks.",
    "topic": "System Design",
    "diff": "Senior",
    "ans": "Ingest webhooks via API Gateway. Push them immediately to an SQS Queue (decoupling). Have a fleet of Lambda functions or Workers pull from SQS to process them asynchronously. Use a Dead Letter Queue (DLQ) for failures.",
    "keys": "Decoupling, SQS, Asynchronous, DLQ, Scalability"
  },
  {
    "q": "What is 'Sharding' in a database?",
    "topic": "Database Architecture",
    "diff": "Senior",
    "ans": "Splitting a large database horizontally across multiple servers (shards) based on a 'Shard Key' (e.g., UserID). This allows writing to multiple servers simultaneously, overcoming single-server write limits.",
    "keys": "Horizontal partitioning, Write scaling, Shard Key"
  },
  {
    "q": "Explain CDN (Content Delivery Network) caching strategies.",
    "topic": "Web Performance",
    "diff": "Mid",
    "ans": "Use 'Cache-Control' headers. 'TTL' (Time To Live) determines how long content stays. Invalidate cache when content updates. Use 'Origin Shield' to protect the backend.",
    "keys": "TTL, Cache invalidation, Edge locations, Latency"
  },
  {
    "q": "How do you design for failure in the cloud?",
    "topic": "Cloud Architecture",
    "diff": "Senior",
    "ans": "Assume everything fails. Use Multi-AZ for redundancy. Use Auto Scaling for capacity replacement. Use Decoupling (Queues) so one component failure doesn't crash the whole flow. Use Chaos Engineering to test.",
    "keys": "Redundancy, Decoupling, Auto Scaling, Chaos Engineering"
  },
  {
    "q": "What is Idempotency in API design?",
    "topic": "API Design",
    "diff": "Senior",
    "ans": "Making the same API call multiple times produces the same result. Example: 'Payment' API should check a unique 'TransactionID'. If called twice, it shouldn't charge the user twice.",
    "keys": "Safe retries, Unique ID, Consistency, REST API"
  },
  {
    "q": "Difference between Monolith and Microservices?",
    "topic": "Architecture",
    "diff": "Mid",
    "ans": "Monolith: Single codebase, single deployment unit, easy to debug but hard to scale. Microservices: Loosely coupled services, independent deployment, hard to debug (distributed tracing needed) but scales well.",
    "keys": "Coupling, Deployment, Complexity vs Scale"
  },
  {
    "q": "How does SSL/TLS Offloading work?",
    "topic": "Networking Design",
    "diff": "Mid",
    "ans": "Decryption is CPU intensive. The Load Balancer decrypts the HTTPS traffic and sends HTTP to the backend servers. This frees up the backend servers' CPU to focus on application logic.",
    "keys": "Load Balancer, Decryption, CPU optimization, Security trade-off"
  },
  {
    "q": "What is 'Blue-Green' vs 'Canary' deployment?",
    "topic": "DevOps",
    "diff": "Mid",
    "ans": "Blue-Green: Instant switch of 100% traffic from old env to new env. Canary: Gradual shift (5%, 10%, 50%) to the new version based on health metrics.",
    "keys": "Traffic shifting, Risk mitigation, Deployment strategies"
  },
  {
    "q": "What is Infrastructure as Code (IaC)?",
    "topic": "DevOps",
    "diff": "Junior",
    "ans": "Managing infrastructure (servers, networks) using code (Terraform, CloudFormation) rather than manual configuration. Allows version control, reproducibility, and automation.",
    "keys": "Terraform, Version Control, Automation, Reproducibility"
  },
  {
    "q": "What is a 'Stateless' application?",
    "topic": "Cloud Architecture",
    "diff": "Mid",
    "ans": "An app that does not store client data (session) on the server itself. Session state is stored in an external DB or Redis. This allows any server to handle any request, enabling easy scaling.",
    "keys": "Scaling, External state, Redis, Load balancing"
  },
  {
    "q": "Explain the 'Shared Responsibility Model'.",
    "topic": "Cloud Security",
    "diff": "Junior",
    "ans": "Cloud Provider manages 'Security OF the cloud' (Hardware, Data Centers). Customer manages 'Security IN the cloud' (Data, OS patching, IAM, Firewalls).",
    "keys": "AWS/Azure, Compliance, Security boundary"
  },
  {
    "q": "What is a 'Dead Letter Queue' (DLQ)?",
    "topic": "System Design",
    "diff": "Mid",
    "ans": "A queue where messages are sent if they cannot be processed successfully after max retries. It allows engineers to inspect and debug failed messages without blocking the main queue.",
    "keys": "Error handling, Debugging, SQS/Lambda"
  },
  {
    "q": "How do you ensure Zero Downtime deployment?",
    "topic": "DevOps",
    "diff": "Senior",
    "ans": "Use Rolling Updates (replace pods one by one) or Blue/Green deployment. Ensure database schema changes are backward compatible.",
    "keys": "Rolling update, Backward compatibility, Availability"
  },
  {
    "q": "What is the difference between Logging and Monitoring?",
    "topic": "Observability",
    "diff": "Junior",
    "ans": "Monitoring tells you *when* something is wrong (metrics/alerts, e.g., 'High CPU'). Logging tells you *why* it is wrong (detailed error messages/stack traces).",
    "keys": "Metrics vs Logs, When vs Why, Alerting, Debugging"
  },
  {
    "q": "Explain the 4 Golden Signals of monitoring.",
    "topic": "SRE",
    "diff": "Senior",
    "ans": "Latency (time to serve request), Traffic (demand/req per sec), Errors (fail rate), and Saturation (how full the system is, e.g., queue depth).",
    "keys": "Latency, Traffic, Errors, Saturation, Google SRE"
  },
  {
    "q": "What is the difference between a 'Counter' and a 'Gauge' metric in Prometheus?",
    "topic": "Observability",
    "diff": "Mid",
    "ans": "A Counter only goes up (cumulative, e.g., Total Requests). A Gauge can go up and down (snapshot, e.g., Current Memory Usage).",
    "keys": "Prometheus types, Monotonically increasing, Snapshot, Metric types"
  },
  {
    "q": "How does Distributed Tracing (e.g., Jaeger/OpenTelemetry) work?",
    "topic": "Observability",
    "diff": "Senior",
    "ans": "It attaches a unique 'Trace ID' to a request as it enters the system. This ID is passed between microservices (via headers). Tracing tools collect these spans to visualize the full journey and find latency bottlenecks.",
    "keys": "Trace ID, Spans, Context propagation, Latency analysis"
  },
  {
    "q": "What is the ELK Stack?",
    "topic": "Observability",
    "diff": "Mid",
    "ans": "Elasticsearch (Search engine), Logstash (Ingest pipeline), and Kibana (Visualization). It is used for centralized logging. A common variation is EFK (using Fluentd instead of Logstash).",
    "keys": "Centralized logging, Search, Visualization, Ingestion"
  },
  {
    "q": "How do you alert on a 'High Error Rate' using PromQL?",
    "topic": "Observability",
    "diff": "Senior",
    "ans": "Calculate the rate of 500 errors divided by total requests. Example: `rate(http_requests_total{status='500'}[5m]) / rate(http_requests_total[5m]) > 0.05` (meaning > 5% error rate).",
    "keys": "PromQL, Rate function, Threshold, Alerting rule"
  },
  {
    "q": "What is 'Cardinality' in metrics and why is high cardinality bad?",
    "topic": "Observability",
    "diff": "Senior",
    "ans": "Cardinality is the number of unique combinations of metric labels. High cardinality (e.g., using UserID or IP as a label) explodes the database size and slows down queries, potentially crashing the monitoring system.",
    "keys": "Unique labels, Performance impact, TSDB explosion, Label design"
  },
  {
    "q": "What is a 'Synthetic Monitor'?",
    "topic": "Observability",
    "diff": "Mid",
    "ans": "A script that simulates user behavior (e.g., logging in and checking a dashboard) at regular intervals to verify the system is working from the outside, even if no real users are active.",
    "keys": "Proactive monitoring, User simulation, Uptime check, E2E test"
  },
  {
    "q": "Explain 'Log Rotation'.",
    "topic": "Linux Admin",
    "diff": "Junior",
    "ans": "The process of archiving old log files and creating new ones (e.g., daily or by size) to prevent logs from consuming all disk space. Tools like `logrotate` manage this.",
    "keys": "Disk space management, Archiving, logrotate, Compression"
  },
  {
    "q": "What is 'Push' vs 'Pull' monitoring?",
    "topic": "Observability",
    "diff": "Mid",
    "ans": "Pull (Prometheus): The server scrapes metrics from the app endpoints. Push (DataDog/Graphite): The app sends metrics to the server. Pull is better for knowing if a service is down; Push is better for short-lived batch jobs.",
    "keys": "Scraping vs Sending, Service discovery, Batch jobs"
  },
  {
    "q": "What is BGP (Border Gateway Protocol)?",
    "topic": "Networking",
    "diff": "Senior",
    "ans": "BGP is the protocol used to route traffic between different Autonomous Systems (AS) on the internet. It picks the most efficient path. In Cloud, it's used for Direct Connect routing.",
    "keys": "Routing protocol, Autonomous Systems, Internet backbone, Direct Connect"
  },
  {
    "q": "Difference between TCP Keepalive and HTTP Keep-Alive?",
    "topic": "Networking",
    "diff": "Senior",
    "ans": "TCP Keepalive is a packet sent to check if the connection is still open. HTTP Keep-Alive is a header instructing the server to keep the connection open for subsequent requests (reusing the TCP connection) to reduce latency.",
    "keys": "Connection check vs Connection reuse, Latency reduction, Headers"
  },
  {
    "q": "What is a Subnet Mask (e.g., /24)?",
    "topic": "Networking",
    "diff": "Junior",
    "ans": "It defines the boundary of the network. A /24 mask (255.255.255.0) means the first 3 octets identify the network, and the last octet identifies the host (allowing 254 hosts).",
    "keys": "IP addressing, Network boundary, Host capacity, CIDR"
  },
  {
    "q": "Explain 'Split Tunneling' in a VPN.",
    "topic": "Networking",
    "diff": "Mid",
    "ans": "Split tunneling routes only corporate traffic through the VPN, while letting general internet traffic (like YouTube) go through the user's local ISP. This saves VPN bandwidth and reduces latency.",
    "keys": "Traffic routing, Bandwidth optimization, Security trade-off"
  },
  {
    "q": "What is the OSI Model? Name the layers.",
    "topic": "Networking",
    "diff": "Junior",
    "ans": "7. Application (HTTP), 6. Presentation (SSL), 5. Session, 4. Transport (TCP/UDP), 3. Network (IP), 2. Data Link (MAC), 1. Physical (Cable).",
    "keys": "7 Layers, Encapsulation, Troubleshooting model"
  },
  {
    "q": "How does a 'Sticky Session' (Session Affinity) work?",
    "topic": "Networking",
    "diff": "Mid",
    "ans": "The Load Balancer uses a cookie or source IP to ensure a specific user is always routed to the *same* backend server. Useful for apps that store session data locally on the server (not recommended for cloud-native).",
    "keys": "Load Balancer, Cookies, State persistence, Scaling limitation"
  },
  {
    "q": "What is an 'Ephemeral Port'?",
    "topic": "Networking",
    "diff": "Mid",
    "ans": "A temporary high-numbered port (usually 1024-65535) assigned by the OS to the client side of a TCP connection. The server listens on a well-known port (80), the client talks from an ephemeral port.",
    "keys": "Temporary port, Client-side, TCP connection, Range"
  },
  {
    "q": "What is ARP (Address Resolution Protocol)?",
    "topic": "Networking",
    "diff": "Junior",
    "ans": "ARP translates an IP address (Layer 3) into a MAC address (Layer 2) so devices can communicate on the local network (LAN).",
    "keys": "IP to MAC, Layer 2 vs Layer 3, LAN communication"
  },
  {
    "q": "Why would you use a VPC Peering connection vs Transit Gateway?",
    "topic": "AWS Networking",
    "diff": "Senior",
    "ans": "VPC Peering is a 1-to-1 direct connection; it's non-transitive (A connected to B and B to C doesn't mean A connects to C). Transit Gateway is a hub that connects hundreds of VPCs transitively. Use TGW for complex networks.",
    "keys": "1-to-1 vs Hub-and-Spoke, Transitive routing, Scalability"
  },
  {
    "q": "What is 'Anycast' DNS?",
    "topic": "Networking",
    "diff": "Senior",
    "ans": "A routing method where the same IP address exists at multiple locations. The network routes the user to the *nearest* location. This improves speed and redundancy for DNS (like Route 53 or 8.8.8.8).",
    "keys": "Routing topology, Latency reduction, Redundancy, Nearest node"
  },
  {
    "q": "Difference between `git merge` and `git rebase`?",
    "topic": "Git",
    "diff": "Mid",
    "ans": "Merge creates a new commit combining histories, preserving the exact history structure (good for public branches). Rebase rewrites history to make it linear by moving your commits to the tip of the master (cleaner history, good for local cleanup).",
    "keys": "History preservation vs Linear history, Commit rewriting, Conflicts"
  },
  {
    "q": "What is a 'detached HEAD' state in Git?",
    "topic": "Git",
    "diff": "Mid",
    "ans": "It means you checked out a specific commit hash (or tag) instead of a branch name. You are looking at a snapshot of the past. New commits here won't belong to any branch and will be lost if you switch away.",
    "keys": "No branch, Snapshot, Lost commits, Checkout hash"
  },
  {
    "q": "How do you undo the last commit but keep the changes in your files?",
    "topic": "Git",
    "diff": "Junior",
    "ans": "Use `git reset --soft HEAD~1`. This moves the pointer back one step but leaves the files in the 'Staging Area'.",
    "keys": "git reset soft, Staging area, Undo commit"
  },
  {
    "q": "What is `git cherry-pick`?",
    "topic": "Git",
    "diff": "Mid",
    "ans": "It allows you to take a specific commit from one branch and apply it to another branch, without merging the entire branch. Useful for hotfixes.",
    "keys": "Selective merge, Hotfix, Commit hash"
  },
  {
    "q": "What is `.gitignore` and does it remove files already tracked?",
    "topic": "Git",
    "diff": "Junior",
    "ans": "It lists patterns of files (like build artifacts, secrets) that Git should ignore. It does NOT remove files that were already committed; you must use `git rm --cached` to stop tracking them.",
    "keys": "Ignore patterns, Untracked files, git rm cached"
  },
  {
    "q": "Explain 'Git Flow' branching strategy.",
    "topic": "Git",
    "diff": "Mid",
    "ans": "A strict model with specific branches: 'Master' (Prod), 'Develop' (Integration), 'Feature' (New work), 'Release' (Prep for prod), and 'Hotfix' (Urgent prod fixes).",
    "keys": "Master/Develop/Feature, Structured workflow, Release management"
  },
  {
    "q": "What is the 'Staging Area' (Index) in Git?",
    "topic": "Git",
    "diff": "Junior",
    "ans": "It's the middle ground between your working directory and the repository. You 'add' files to the stage before you 'commit' them. It allows you to craft commits carefully.",
    "keys": "git add, Pre-commit, File tracking"
  },
  {
    "q": "How do you resolve a Merge Conflict?",
    "topic": "Git",
    "diff": "Junior",
    "ans": "Git pauses the merge and marks the conflicting files. You must manually edit the files to choose the correct code (Current Change vs Incoming Change), remove conflict markers (`<<<<`), add the file, and commit.",
    "keys": "Manual intervention, Conflict markers, Resolution"
  },
  {
    "q": "What is the difference between a 'Fork' and a 'Branch'?",
    "topic": "Git",
    "diff": "Junior",
    "ans": "A Branch is a separate line of development *within* the same repository. A Fork is a complete copy of the *entire* repository on your own account, used for contributing to open source projects via Pull Requests.",
    "keys": "Same repo vs Copy repo, Open Source, Pull Requests"
  },
  {
    "q": "What does `git stash` do?",
    "topic": "Git",
    "diff": "Junior",
    "ans": "It temporarily shelves (saves) your uncommitted changes so you can switch branches to work on something else. You can bring them back later with `git stash pop`.",
    "keys": "Temporary save, Context switching, Clean working directory"
  },
  {
    "q": "How do you reduce the attack surface of a Docker container?",
    "topic": "Container Security",
    "diff": "Senior",
    "ans": "Use minimal base images (Alpine/Distroless). Do NOT run as root (`USER app`). Scan images for CVEs. Remove shell access/debugging tools. Limit resource usage (CPU/RAM).",
    "keys": "Minimal image, Non-root user, Vulnerability scanning, Least privilege"
  },
  {
    "q": "What is 'Distroless' image?",
    "topic": "Container Security",
    "diff": "Senior",
    "ans": "A container image containing only the application and its runtime dependencies. It has NO package manager, shell, or other standard Linux tools, making it very secure and small.",
    "keys": "No shell, No package manager, Security hardening, Small footprint"
  },
  {
    "q": "What is Image Signing (e.g., Docker Content Trust)?",
    "topic": "Security",
    "diff": "Senior",
    "ans": "It uses digital signatures to verify that the container image you are pulling is exactly what the publisher built and hasn't been tampered with or replaced by a malicious actor.",
    "keys": "Digital signature, Integrity check, Supply chain security"
  },
  {
    "q": "Explain 'Secret Sprawl'.",
    "topic": "Security",
    "diff": "Mid",
    "ans": "The accidental spreading of API keys and passwords across codebases, git history, log files, and chat apps. It makes rotating secrets difficult and increases breach risk.",
    "keys": "Leakage, Hardcoded secrets, Git history, Risk management"
  },
  {
    "q": "What is 'Runtime Security' in containers (e.g., Falco)?",
    "topic": "Container Security",
    "diff": "Senior",
    "ans": "Scanning images happens *before* deployment. Runtime security monitors the container *while it runs*, looking for suspicious behavior like a web server suddenly spawning a shell or accessing sensitive files.",
    "keys": "Behavioral monitoring, Anomaly detection, Falco, Real-time"
  },
  {
    "q": "When should you use AWS Fargate instead of standard EC2 or Lambda?",
    "topic": "Serverless",
    "diff": "Mid",
    "ans": "Use Fargate when you need long-running containers but don't want to manage the underlying servers (patching/scaling nodes). Use Lambda for short-lived, event-driven tasks. Use EC2 when you need persistent disk access or specific kernel tuning.",
    "keys": "Serverless Containers, Long-running, No management, vs Lambda"
  },
  {
    "q": "What is the 'EventBridge' service used for?",
    "topic": "Serverless",
    "diff": "Mid",
    "ans": "It is a serverless event bus that connects app data from your own apps, SaaS apps, and AWS services. It replaces complex point-to-point connections with a central router that filters and delivers events.",
    "keys": "Event Bus, Decoupling, SaaS integration, Rules/Filtering"
  },
  {
    "q": "Explain AWS Step Functions.",
    "topic": "Serverless",
    "diff": "Senior",
    "ans": "A serverless orchestration service that lets you coordinate multiple Lambda functions into workflows (State Machines). It handles retries, parallel execution, and error handling natively, so you don't write that logic in code.",
    "keys": "Orchestration, State Machine, Workflows, Visual"
  },
  {
    "q": "How do you handle 'Partial Failures' in a batch of SQS messages triggered by Lambda?",
    "topic": "Serverless",
    "diff": "Senior",
    "ans": "By default, if one message fails, the whole batch retries. To fix this, enable 'Report Batch Item Failures' in the Lambda event source mapping. The Lambda returns the ID of the specific failed message so only that one is retried.",
    "keys": "Batch Item Failures, Partial retry, Idempotency"
  },
  {
    "q": "What is the difference between Kinesis Data Streams and SQS?",
    "topic": "Data Engineering",
    "diff": "Mid",
    "ans": "SQS is for simple message queuing (one consumer deletes the message). Kinesis is for real-time data streaming (multiple consumers can read the same data stream independently, replay capability).",
    "keys": "Stream vs Queue, Replay, Real-time analytics, Multiple consumers"
  },
  {
    "q": "What limits exist on AWS Lambda?",
    "topic": "Serverless",
    "diff": "Junior",
    "ans": "Execution timeout (15 mins), Memory (10GB), Payload size (6MB sync / 256KB async), and Concurrency limits (1000 default per region).",
    "keys": "15 min timeout, Memory limit, Payload size, Concurrency"
  },
  {
    "q": "Explain the 'Saga Pattern' in serverless microservices.",
    "topic": "Architecture Patterns",
    "diff": "Senior",
    "ans": "A pattern to manage distributed transactions. If a step fails (e.g., 'Payment Charged'), the Saga executes a 'Compensating Transaction' (e.g., 'Refund Payment') to undo the changes, ensuring data consistency.",
    "keys": "Distributed transaction, Compensating transaction, Rollback"
  },
  {
    "q": "What is 'Provisioned Concurrency' in Lambda?",
    "topic": "Serverless",
    "diff": "Mid",
    "ans": "It keeps a specific number of Lambda environments initialized and ready to respond in double-digit milliseconds. It eliminates 'Cold Starts' for latency-sensitive applications.",
    "keys": "Cold start elimination, Pre-warmed, Latency sensitive"
  },
  {
    "q": "How does API Gateway 'Throttling' work?",
    "topic": "Serverless",
    "diff": "Mid",
    "ans": "It limits the number of requests per second (RPS) a user or tenant can make. It protects the backend from being overwhelmed. You can set limits at the API level or per Usage Plan (API Key).",
    "keys": "Rate limiting, DDoS protection, Usage Plans, 429 Too Many Requests"
  },
  {
    "q": "What is the difference between Standard and FIFO SQS queues?",
    "topic": "Serverless",
    "diff": "Junior",
    "ans": "Standard offers 'At-Least-Once' delivery and best-effort ordering (fast). FIFO (First-In-First-Out) guarantees 'Exactly-Once' delivery and strict ordering but has lower throughput (300/3000 TPS).",
    "keys": "Ordering, Duplication, Throughput limits, Exactly-once"
  },
  {
    "q": "How do you secure an internal API Gateway?",
    "topic": "Security",
    "diff": "Mid",
    "ans": "Use a 'Private' API Gateway endpoint accessible only from within a VPC. Use Resource Policies to whitelist specific VPC IDs or Source IPs.",
    "keys": "Private Endpoint, VPC Link, Resource Policy"
  },
  {
    "q": "What is DynamoDB Streams?",
    "topic": "Database",
    "diff": "Mid",
    "ans": "A feature that captures a time-ordered sequence of item-level modifications (insert/update/delete) in a table. It allows you to trigger a Lambda function immediately after a DB change (CDC - Change Data Capture).",
    "keys": "Change Data Capture, Triggers, Event-driven DB"
  },
  {
    "q": "Why would you use AWS Glue?",
    "topic": "Data Engineering",
    "diff": "Mid",
    "ans": "Glue is a serverless ETL (Extract, Transform, Load) service. It discovers data (Crawlers), catalogs it, and prepares it for analytics (using PySpark jobs) without managing servers.",
    "keys": "ETL, Serverless, Data Catalog, PySpark"
  },
  {
    "q": "What is an 'Idempotent' Lambda function?",
    "topic": "Serverless",
    "diff": "Senior",
    "ans": "A function that can be run multiple times with the same input without changing the result or causing side effects (e.g., processing the same payment twice). Essential for handling SQS/EventBridge retries.",
    "keys": "Retry safety, No side effects, Consistency"
  },
  {
    "q": "Explain 'Fan-Out' pattern with SNS.",
    "topic": "Architecture",
    "diff": "Junior",
    "ans": "A message is published to one SNS topic, which pushes it to multiple subscribed endpoints (SQS queues, Lambda, Email) simultaneously. This decouples the producer from the consumers.",
    "keys": "One-to-many, Parallel processing, Decoupling"
  },
  {
    "q": "What is a 'Hot Partition' in DynamoDB?",
    "topic": "Database Tuning",
    "diff": "Senior",
    "ans": "When a specific Partition Key is accessed too frequently (e.g., PartitionKey='Status:Active'), causing one partition to exceed its throughput limits while others are idle. Fix by using high-cardinality keys.",
    "keys": "Throttling, Partition Key design, High cardinality, Distribution"
  },
  {
    "q": "Difference between clustered and non-clustered indexes (SQL)?",
    "topic": "Database",
    "diff": "Mid",
    "ans": "Clustered Index determines the physical order of data on disk (only one per table, usually Primary Key). Non-clustered index is a separate structure pointing to the data rows (like a book index).",
    "keys": "Physical order, Lookup speed, B-Tree"
  },
  {
    "q": "When should you use Redis (ElastiCache)?",
    "topic": "Database",
    "diff": "Junior",
    "ans": "Use it for sub-millisecond latency requirements, caching frequent DB queries (Write-Through/Lazy Loading), session storage, or real-time leaderboards. It stores data in memory.",
    "keys": "Caching, In-memory, Sub-millisecond, Session store"
  },
  {
    "q": "What is Database Normalization?",
    "topic": "Database",
    "diff": "Junior",
    "ans": "Structuring a relational database to reduce data redundancy and improve integrity (1NF, 2NF, 3NF). It involves separating data into related tables.",
    "keys": "Redundancy reduction, Data integrity, SQL design"
  },
  {
    "q": "Explain 'Read Replicas' vs 'Multi-AZ' in RDS.",
    "topic": "Database Architecture",
    "diff": "Mid",
    "ans": "Read Replicas are for performance (scaling read traffic asynchronously). Multi-AZ is for disaster recovery (synchronous standby for failover). Multi-AZ does NOT improve performance.",
    "keys": "Scaling vs HA, Async vs Sync, Failover"
  },
  {
    "q": "What is 'ACID' compliance?",
    "topic": "Database",
    "diff": "Junior",
    "ans": "Atomicity (All or nothing), Consistency (Valid data), Isolation (Transactions don't interfere), Durability (Saved permanently). Essential for financial transactions.",
    "keys": "Transaction guarantee, Data integrity, SQL"
  },
  {
    "q": "How does Cassandra/DynamoDB achieve high write speeds?",
    "topic": "Database Internals",
    "diff": "Senior",
    "ans": "They use Log-Structured Merge (LSM) trees and consistent hashing. Writes are appended to a log (fast) rather than updating a B-Tree in place (slower). They trade strict consistency for availability/speed.",
    "keys": "LSM Tree, Append-only, NoSQL design"
  },
  {
    "q": "What is 'Connection Pooling'?",
    "topic": "Database Tuning",
    "diff": "Mid",
    "ans": "A cache of open database connections maintained so that they can be reused. Opening a new TCP connection to a DB is expensive; pooling improves performance significantly (e.g., PgBouncer, RDS Proxy).",
    "keys": "Reuse connections, Performance, RDS Proxy"
  },
  {
    "q": "When would you use a Graph Database (Neptune)?",
    "topic": "Database",
    "diff": "Mid",
    "ans": "When your data is highly interconnected, and you need to query relationships (e.g., Social Networks, Fraud Detection rings, Recommendation engines). SQL joins would be too slow.",
    "keys": "Relationships, Social Network, Fraud Detection, Nodes/Edges"
  },
  {
    "q": "What is the difference between OLTP and OLAP?",
    "topic": "Data Engineering",
    "diff": "Mid",
    "ans": "OLTP (Online Transaction Processing) is for day-to-day operations (fast, small updates, e.g., ATM). OLAP (Online Analytical Processing) is for heavy analysis on historical data (Data Warehouse, Redshift).",
    "keys": "Transactions vs Analysis, Row vs Columnar storage"
  },
  {
    "q": "Explain 'Vacuuming' in PostgreSQL.",
    "topic": "Database Internals",
    "diff": "Senior",
    "ans": "Postgres uses MVCC (Multi-Version Concurrency Control), so updates create new row versions. Old versions ('dead tuples') take up space. Vacuuming reclaims this storage and updates statistics for the query planner.",
    "keys": "Dead tuples, MVCC, Storage reclamation, Maintenance"
  },
  {
    "q": "What is a 'Materialized View'?",
    "topic": "Database Tuning",
    "diff": "Mid",
    "ans": "A database object that stores the result of a query physically. Unlike a standard view (virtual), it doesn't run the query every time you access it, making it much faster for complex aggregations.",
    "keys": "Pre-computed, Performance, Caching query results"
  },
  {
    "q": "What is 'Data Partitioning'?",
    "topic": "Database",
    "diff": "Mid",
    "ans": "Splitting a large table into smaller, manageable pieces (e.g., by Date or Region). This improves query performance because the DB only scans relevant partitions.",
    "keys": "Splitting tables, Query optimization, Manageability"
  },
  {
    "q": "How does a Columnar Database (Redshift) differ from Row-based?",
    "topic": "Database Architecture",
    "diff": "Mid",
    "ans": "Row-based stores data line-by-line (good for fetching a specific user). Columnar stores data column-by-column (good for aggregating 'Total Sales' across a billion rows because it reads less data).",
    "keys": "Analytics, Aggregation speed, Compression"
  },
  {
    "q": "What is 'Database Migration Service' (DMS)?",
    "topic": "Database Operations",
    "diff": "Junior",
    "ans": "A service to migrate relational/NoSQL databases to AWS easily. It supports homogeneous (Oracle to Oracle) and heterogeneous (Oracle to Aurora) migrations with minimal downtime.",
    "keys": "Migration, Replication, Minimal downtime, Schema conversion"
  },
  {
    "q": "What is the difference between Savings Plans and Reserved Instances?",
    "topic": "FinOps",
    "diff": "Mid",
    "ans": "RIs commit to a specific instance type (e.g., m5.large). Savings Plans commit to a specific spend ($10/hour) regardless of instance family or region, offering much more flexibility.",
    "keys": "Commitment model, Flexibility, Cost saving"
  },
  {
    "q": "How do you reduce Data Transfer costs in AWS?",
    "topic": "FinOps",
    "diff": "Senior",
    "ans": "Keep traffic within the same Availability Zone (AZ) where possible. Use VPC Endpoints (PrivateLink) to avoid NAT Gateway charges. Use CloudFront to cache data closer to users.",
    "keys": "Cross-AZ charges, NAT Gateway, VPC Endpoints, CloudFront"
  },
  {
    "q": "What is a 'Spot Instance' and when is it unsafe?",
    "topic": "FinOps",
    "diff": "Junior",
    "ans": "Excess capacity sold cheaply (up to 90% off). Unsafe for stateful apps (Databases) or critical APIs because AWS can terminate them with 2 minutes warning.",
    "keys": "Cost saving, Interruption, Stateless only"
  },
  {
    "q": "How do you track costs per team/project?",
    "topic": "FinOps",
    "diff": "Junior",
    "ans": "Enforce a 'Cost Allocation Tag' strategy (e.g., Tag: Project=FinVerse). Activate these tags in the Billing Console to see a breakdown of costs by tag in Cost Explorer.",
    "keys": "Tagging strategy, Cost Explorer, Attribution"
  },
  {
    "q": "What is AWS Compute Optimizer?",
    "topic": "FinOps",
    "diff": "Mid",
    "ans": "A service that analyzes your resource utilization history (CPU, Memory) and recommends 'Rightsizing' (e.g., downgrading from m5.xlarge to m5.large) to save money.",
    "keys": "Rightsizing, Recommendations, Utilization analysis"
  },
  {
    "q": "Why is NAT Gateway expensive and what is the alternative?",
    "topic": "FinOps",
    "diff": "Senior",
    "ans": "NAT Gateways charge per hour AND per GB processed. For heavy traffic (like S3 uploads from private subnet), use a VPC Endpoint (Gateway Type) for S3, which is free.",
    "keys": "Processing charges, VPC Endpoint S3, Cost avoidance"
  },
  {
    "q": "What is S3 Intelligent-Tiering?",
    "topic": "FinOps",
    "diff": "Mid",
    "ans": "A storage class that automatically moves objects between frequent and infrequent access tiers based on usage patterns, saving money without retrieval fees or operational overhead.",
    "keys": "Automatic tiering, Cost optimization, No overhead"
  },
  {
    "q": "How do you detect 'Zombie' resources?",
    "topic": "FinOps",
    "diff": "Mid",
    "ans": "Use AWS Config or Trusted Advisor to find unattached EBS volumes, unassociated Elastic IPs, and idle Load Balancers. Automate cleanup with Lambda/Systems Manager.",
    "keys": "Unused resources, Waste, Trusted Advisor, Config"
  },
  {
    "q": "Explain the concept of 'Budgets' and 'Anomalies'.",
    "topic": "FinOps",
    "diff": "Junior",
    "ans": "AWS Budgets alert you when forecasted spend exceeds a threshold. Cost Anomaly Detection uses ML to find unusual spikes (e.g., a hacked key mining crypto) and alerts immediately.",
    "keys": "Forecasting, Alerting, ML detection, Security spike"
  },
  {
    "q": "What is the 'Free Tier' myth?",
    "topic": "FinOps",
    "diff": "Junior",
    "ans": "Free Tier expires after 12 months for many services (EC2, RDS). Always set billing alarms immediately on a new account to avoid surprise bills.",
    "keys": "12 month limit, Billing alarms, Surprise bill"
  },
  {
    "q": "Difference between Authentication (AuthN) and Authorization (AuthZ)?",
    "topic": "Security",
    "diff": "Junior",
    "ans": "AuthN verifies WHO you are (Login/MFA). AuthZ verifies WHAT you can do (Permissions/Policies).",
    "keys": "Who vs What, Identity vs Permission"
  },
  {
    "q": "What is OAuth 2.0 vs OIDC (OpenID Connect)?",
    "topic": "Security",
    "diff": "Senior",
    "ans": "OAuth 2.0 is for Authorization (Delegated access, e.g., 'Allow app to access Google Drive'). OIDC is a layer on top of OAuth 2.0 specifically for Authentication (Identity, e.g., 'Log in with Google').",
    "keys": "AuthZ vs AuthN, Access vs Identity, Token types"
  },
  {
    "q": "What is 'Federated Identity'?",
    "topic": "Security",
    "diff": "Mid",
    "ans": "Allowing users to use their existing corporate identity (Active Directory, Okta, Google) to access AWS/Cloud resources without creating a new IAM user. Uses SAML 2.0 or OIDC.",
    "keys": "SAML, SSO, No IAM users, Centralized management"
  },
  {
    "q": "Explain 'Envelope Encryption' (KMS).",
    "topic": "Security",
    "diff": "Senior",
    "ans": "KMS encrypts your data key with a master key (CMK). The data key encrypts your actual data. This hierarchy protects the master key and improves performance for large data.",
    "keys": "Data Key vs Master Key, Hierarchy, Performance"
  },
  {
    "q": "What is a WAF (Web Application Firewall) and what does it block?",
    "topic": "Security",
    "diff": "Mid",
    "ans": "A firewall that inspects HTTP/S traffic at Layer 7. It blocks common attacks like SQL Injection, Cross-Site Scripting (XSS), and bad bots.",
    "keys": "Layer 7, SQLi, XSS, OWASP Top 10"
  },
  {
    "q": "What is GuardDuty?",
    "topic": "Security",
    "diff": "Mid",
    "ans": "A threat detection service that continuously monitors logs (CloudTrail, VPC Flow Logs, DNS) for malicious activity, such as cryptocurrency mining or unauthorized access attempts.",
    "keys": "Threat detection, Log analysis, ML, Crypto mining"
  },
  {
    "q": "How do you ensure compliance with HIPAA/SOC2 on AWS?",
    "topic": "Compliance",
    "diff": "Senior",
    "ans": "Use AWS Artifact to get compliance reports. Enable AWS Config to track configuration history. Encrypt everything at rest and in transit. Enforce Least Privilege.",
    "keys": "Artifact, Config, Encryption, Audit trails"
  },
  {
    "q": "What is 'Secrets Manager' vs 'Parameter Store'?",
    "topic": "Security",
    "diff": "Mid",
    "ans": "Parameter Store is free for standard parameters. Secrets Manager costs money but offers automatic rotation of secrets (changing the DB password automatically) and cross-account access.",
    "keys": "Automatic Rotation, Cost, Simple string vs Secret"
  },
  {
    "q": "Explain 'Cross-Account Access' via IAM Roles.",
    "topic": "Security",
    "diff": "Senior",
    "ans": "Instead of sharing access keys (unsafe), you create an IAM Role in Account B that trusts Account A. A user in Account A 'assumes' the role to perform actions in Account B securely.",
    "keys": "AssumeRole, Trust Policy, No keys shared"
  },
  {
    "q": "What is the purpose of a 'Service Control Policy' (SCP)?",
    "topic": "Security",
    "diff": "Senior",
    "ans": "SCPs are organization-level policies (AWS Organizations). They set the maximum available permissions for an account. Even if an Admin in a child account has 'Allow *', the SCP can block specific actions (e.g., 'Deny turning off CloudTrail').",
    "keys": "Organization level, Guardrails, Limit permissions, Root control"
  }
]