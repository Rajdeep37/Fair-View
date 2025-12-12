import chromadb
import uuid

# 1. Connect
client = chromadb.PersistentClient(path="./interview_db")
collection = client.get_collection("cloud_engineer_questions")

# 2. Define 50 New Questions
serverless_finops_batch = [
    # --- SERVERLESS & EVENT-DRIVEN ARCHITECTURE (15 Questions) ---
    {
        "q": "When should you use AWS Fargate instead of standard EC2 or Lambda?",
        "ans": "Use Fargate when you need long-running containers but don't want to manage the underlying servers (patching/scaling nodes). Use Lambda for short-lived, event-driven tasks. Use EC2 when you need persistent disk access or specific kernel tuning.",
        "keys": "Serverless Containers, Long-running, No management, vs Lambda",
        "topic": "Serverless", "diff": "Mid"
    },
    {
        "q": "What is the 'EventBridge' service used for?",
        "ans": "It is a serverless event bus that connects app data from your own apps, SaaS apps, and AWS services. It replaces complex point-to-point connections with a central router that filters and delivers events.",
        "keys": "Event Bus, Decoupling, SaaS integration, Rules/Filtering",
        "topic": "Serverless", "diff": "Mid"
    },
    {
        "q": "Explain AWS Step Functions.",
        "ans": "A serverless orchestration service that lets you coordinate multiple Lambda functions into workflows (State Machines). It handles retries, parallel execution, and error handling natively, so you don't write that logic in code.",
        "keys": "Orchestration, State Machine, Workflows, Visual",
        "topic": "Serverless", "diff": "Senior"
    },
    {
        "q": "How do you handle 'Partial Failures' in a batch of SQS messages triggered by Lambda?",
        "ans": "By default, if one message fails, the whole batch retries. To fix this, enable 'Report Batch Item Failures' in the Lambda event source mapping. The Lambda returns the ID of the specific failed message so only that one is retried.",
        "keys": "Batch Item Failures, Partial retry, Idempotency",
        "topic": "Serverless", "diff": "Senior"
    },
    {
        "q": "What is the difference between Kinesis Data Streams and SQS?",
        "ans": "SQS is for simple message queuing (one consumer deletes the message). Kinesis is for real-time data streaming (multiple consumers can read the same data stream independently, replay capability).",
        "keys": "Stream vs Queue, Replay, Real-time analytics, Multiple consumers",
        "topic": "Data Engineering", "diff": "Mid"
    },
    {
        "q": "What limits exist on AWS Lambda?",
        "ans": "Execution timeout (15 mins), Memory (10GB), Payload size (6MB sync / 256KB async), and Concurrency limits (1000 default per region).",
        "keys": "15 min timeout, Memory limit, Payload size, Concurrency",
        "topic": "Serverless", "diff": "Junior"
    },
    {
        "q": "Explain the 'Saga Pattern' in serverless microservices.",
        "ans": "A pattern to manage distributed transactions. If a step fails (e.g., 'Payment Charged'), the Saga executes a 'Compensating Transaction' (e.g., 'Refund Payment') to undo the changes, ensuring data consistency.",
        "keys": "Distributed transaction, Compensating transaction, Rollback",
        "topic": "Architecture Patterns", "diff": "Senior"
    },
    {
        "q": "What is 'Provisioned Concurrency' in Lambda?",
        "ans": "It keeps a specific number of Lambda environments initialized and ready to respond in double-digit milliseconds. It eliminates 'Cold Starts' for latency-sensitive applications.",
        "keys": "Cold start elimination, Pre-warmed, Latency sensitive",
        "topic": "Serverless", "diff": "Mid"
    },
    {
        "q": "How does API Gateway 'Throttling' work?",
        "ans": "It limits the number of requests per second (RPS) a user or tenant can make. It protects the backend from being overwhelmed. You can set limits at the API level or per Usage Plan (API Key).",
        "keys": "Rate limiting, DDoS protection, Usage Plans, 429 Too Many Requests",
        "topic": "Serverless", "diff": "Mid"
    },
    {
        "q": "What is the difference between Standard and FIFO SQS queues?",
        "ans": "Standard offers 'At-Least-Once' delivery and best-effort ordering (fast). FIFO (First-In-First-Out) guarantees 'Exactly-Once' delivery and strict ordering but has lower throughput (300/3000 TPS).",
        "keys": "Ordering, Duplication, Throughput limits, Exactly-once",
        "topic": "Serverless", "diff": "Junior"
    },
    {
        "q": "How do you secure an internal API Gateway?",
        "ans": "Use a 'Private' API Gateway endpoint accessible only from within a VPC. Use Resource Policies to whitelist specific VPC IDs or Source IPs.",
        "keys": "Private Endpoint, VPC Link, Resource Policy",
        "topic": "Security", "diff": "Mid"
    },
    {
        "q": "What is DynamoDB Streams?",
        "ans": "A feature that captures a time-ordered sequence of item-level modifications (insert/update/delete) in a table. It allows you to trigger a Lambda function immediately after a DB change (CDC - Change Data Capture).",
        "keys": "Change Data Capture, Triggers, Event-driven DB",
        "topic": "Database", "diff": "Mid"
    },
    {
        "q": "Why would you use AWS Glue?",
        "ans": "Glue is a serverless ETL (Extract, Transform, Load) service. It discovers data (Crawlers), catalogs it, and prepares it for analytics (using PySpark jobs) without managing servers.",
        "keys": "ETL, Serverless, Data Catalog, PySpark",
        "topic": "Data Engineering", "diff": "Mid"
    },
    {
        "q": "What is an 'Idempotent' Lambda function?",
        "ans": "A function that can be run multiple times with the same input without changing the result or causing side effects (e.g., processing the same payment twice). Essential for handling SQS/EventBridge retries.",
        "keys": "Retry safety, No side effects, Consistency",
        "topic": "Serverless", "diff": "Senior"
    },
    {
        "q": "Explain 'Fan-Out' pattern with SNS.",
        "ans": "A message is published to one SNS topic, which pushes it to multiple subscribed endpoints (SQS queues, Lambda, Email) simultaneously. This decouples the producer from the consumers.",
        "keys": "One-to-many, Parallel processing, Decoupling",
        "topic": "Architecture", "diff": "Junior"
    },

    # --- DATABASE PERFORMANCE & TUNING (15 Questions) ---
    {
        "q": "What is a 'Hot Partition' in DynamoDB?",
        "ans": "When a specific Partition Key is accessed too frequently (e.g., PartitionKey='Status:Active'), causing one partition to exceed its throughput limits while others are idle. Fix by using high-cardinality keys.",
        "keys": "Throttling, Partition Key design, High cardinality, Distribution",
        "topic": "Database Tuning", "diff": "Senior"
    },
    {
        "q": "Difference between clustered and non-clustered indexes (SQL)?",
        "ans": "Clustered Index determines the physical order of data on disk (only one per table, usually Primary Key). Non-clustered index is a separate structure pointing to the data rows (like a book index).",
        "keys": "Physical order, Lookup speed, B-Tree",
        "topic": "Database", "diff": "Mid"
    },
    {
        "q": "When should you use Redis (ElastiCache)?",
        "ans": "Use it for sub-millisecond latency requirements, caching frequent DB queries (Write-Through/Lazy Loading), session storage, or real-time leaderboards. It stores data in memory.",
        "keys": "Caching, In-memory, Sub-millisecond, Session store",
        "topic": "Database", "diff": "Junior"
    },
    {
        "q": "What is Database Normalization?",
        "ans": "Structuring a relational database to reduce data redundancy and improve integrity (1NF, 2NF, 3NF). It involves separating data into related tables.",
        "keys": "Redundancy reduction, Data integrity, SQL design",
        "topic": "Database", "diff": "Junior"
    },
    {
        "q": "Explain 'Read Replicas' vs 'Multi-AZ' in RDS.",
        "ans": "Read Replicas are for performance (scaling read traffic asynchronously). Multi-AZ is for disaster recovery (synchronous standby for failover). Multi-AZ does NOT improve performance.",
        "keys": "Scaling vs HA, Async vs Sync, Failover",
        "topic": "Database Architecture", "diff": "Mid"
    },
    {
        "q": "What is 'ACID' compliance?",
        "ans": "Atomicity (All or nothing), Consistency (Valid data), Isolation (Transactions don't interfere), Durability (Saved permanently). Essential for financial transactions.",
        "keys": "Transaction guarantee, Data integrity, SQL",
        "topic": "Database", "diff": "Junior"
    },
    {
        "q": "How does Cassandra/DynamoDB achieve high write speeds?",
        "ans": "They use Log-Structured Merge (LSM) trees and consistent hashing. Writes are appended to a log (fast) rather than updating a B-Tree in place (slower). They trade strict consistency for availability/speed.",
        "keys": "LSM Tree, Append-only, NoSQL design",
        "topic": "Database Internals", "diff": "Senior"
    },
    {
        "q": "What is 'Connection Pooling'?",
        "ans": "A cache of open database connections maintained so that they can be reused. Opening a new TCP connection to a DB is expensive; pooling improves performance significantly (e.g., PgBouncer, RDS Proxy).",
        "keys": "Reuse connections, Performance, RDS Proxy",
        "topic": "Database Tuning", "diff": "Mid"
    },
    {
        "q": "When would you use a Graph Database (Neptune)?",
        "ans": "When your data is highly interconnected, and you need to query relationships (e.g., Social Networks, Fraud Detection rings, Recommendation engines). SQL joins would be too slow.",
        "keys": "Relationships, Social Network, Fraud Detection, Nodes/Edges",
        "topic": "Database", "diff": "Mid"
    },
    {
        "q": "What is the difference between OLTP and OLAP?",
        "ans": "OLTP (Online Transaction Processing) is for day-to-day operations (fast, small updates, e.g., ATM). OLAP (Online Analytical Processing) is for heavy analysis on historical data (Data Warehouse, Redshift).",
        "keys": "Transactions vs Analysis, Row vs Columnar storage",
        "topic": "Data Engineering", "diff": "Mid"
    },
    {
        "q": "Explain 'Vacuuming' in PostgreSQL.",
        "ans": "Postgres uses MVCC (Multi-Version Concurrency Control), so updates create new row versions. Old versions ('dead tuples') take up space. Vacuuming reclaims this storage and updates statistics for the query planner.",
        "keys": "Dead tuples, MVCC, Storage reclamation, Maintenance",
        "topic": "Database Internals", "diff": "Senior"
    },
    {
        "q": "What is a 'Materialized View'?",
        "ans": "A database object that stores the result of a query physically. Unlike a standard view (virtual), it doesn't run the query every time you access it, making it much faster for complex aggregations.",
        "keys": "Pre-computed, Performance, Caching query results",
        "topic": "Database Tuning", "diff": "Mid"
    },
    {
        "q": "What is 'Data Partitioning'?",
        "ans": "Splitting a large table into smaller, manageable pieces (e.g., by Date or Region). This improves query performance because the DB only scans relevant partitions.",
        "keys": "Splitting tables, Query optimization, Manageability",
        "topic": "Database", "diff": "Mid"
    },
    {
        "q": "How does a Columnar Database (Redshift) differ from Row-based?",
        "ans": "Row-based stores data line-by-line (good for fetching a specific user). Columnar stores data column-by-column (good for aggregating 'Total Sales' across a billion rows because it reads less data).",
        "keys": "Analytics, Aggregation speed, Compression",
        "topic": "Database Architecture", "diff": "Mid"
    },
    {
        "q": "What is 'Database Migration Service' (DMS)?",
        "ans": "A service to migrate relational/NoSQL databases to AWS easily. It supports homogeneous (Oracle to Oracle) and heterogeneous (Oracle to Aurora) migrations with minimal downtime.",
        "keys": "Migration, Replication, Minimal downtime, Schema conversion",
        "topic": "Database Operations", "diff": "Junior"
    },

    # --- FINOPS & COST OPTIMIZATION (10 Questions) ---
    {
        "q": "What is the difference between Savings Plans and Reserved Instances?",
        "ans": "RIs commit to a specific instance type (e.g., m5.large). Savings Plans commit to a specific spend ($10/hour) regardless of instance family or region, offering much more flexibility.",
        "keys": "Commitment model, Flexibility, Cost saving",
        "topic": "FinOps", "diff": "Mid"
    },
    {
        "q": "How do you reduce Data Transfer costs in AWS?",
        "ans": "Keep traffic within the same Availability Zone (AZ) where possible. Use VPC Endpoints (PrivateLink) to avoid NAT Gateway charges. Use CloudFront to cache data closer to users.",
        "keys": "Cross-AZ charges, NAT Gateway, VPC Endpoints, CloudFront",
        "topic": "FinOps", "diff": "Senior"
    },
    {
        "q": "What is a 'Spot Instance' and when is it unsafe?",
        "ans": "Excess capacity sold cheaply (up to 90% off). Unsafe for stateful apps (Databases) or critical APIs because AWS can terminate them with 2 minutes warning.",
        "keys": "Cost saving, Interruption, Stateless only",
        "topic": "FinOps", "diff": "Junior"
    },
    {
        "q": "How do you track costs per team/project?",
        "ans": "Enforce a 'Cost Allocation Tag' strategy (e.g., Tag: Project=FinVerse). Activate these tags in the Billing Console to see a breakdown of costs by tag in Cost Explorer.",
        "keys": "Tagging strategy, Cost Explorer, Attribution",
        "topic": "FinOps", "diff": "Junior"
    },
    {
        "q": "What is AWS Compute Optimizer?",
        "ans": "A service that analyzes your resource utilization history (CPU, Memory) and recommends 'Rightsizing' (e.g., downgrading from m5.xlarge to m5.large) to save money.",
        "keys": "Rightsizing, Recommendations, Utilization analysis",
        "topic": "FinOps", "diff": "Mid"
    },
    {
        "q": "Why is NAT Gateway expensive and what is the alternative?",
        "ans": "NAT Gateways charge per hour AND per GB processed. For heavy traffic (like S3 uploads from private subnet), use a VPC Endpoint (Gateway Type) for S3, which is free.",
        "keys": "Processing charges, VPC Endpoint S3, Cost avoidance",
        "topic": "FinOps", "diff": "Senior"
    },
    {
        "q": "What is S3 Intelligent-Tiering?",
        "ans": "A storage class that automatically moves objects between frequent and infrequent access tiers based on usage patterns, saving money without retrieval fees or operational overhead.",
        "keys": "Automatic tiering, Cost optimization, No overhead",
        "topic": "FinOps", "diff": "Mid"
    },
    {
        "q": "How do you detect 'Zombie' resources?",
        "ans": "Use AWS Config or Trusted Advisor to find unattached EBS volumes, unassociated Elastic IPs, and idle Load Balancers. Automate cleanup with Lambda/Systems Manager.",
        "keys": "Unused resources, Waste, Trusted Advisor, Config",
        "topic": "FinOps", "diff": "Mid"
    },
    {
        "q": "Explain the concept of 'Budgets' and 'Anomalies'.",
        "ans": "AWS Budgets alert you when forecasted spend exceeds a threshold. Cost Anomaly Detection uses ML to find unusual spikes (e.g., a hacked key mining crypto) and alerts immediately.",
        "keys": "Forecasting, Alerting, ML detection, Security spike",
        "topic": "FinOps", "diff": "Junior"
    },
    {
        "q": "What is the 'Free Tier' myth?",
        "ans": "Free Tier expires after 12 months for many services (EC2, RDS). Always set billing alarms immediately on a new account to avoid surprise bills.",
        "keys": "12 month limit, Billing alarms, Surprise bill",
        "topic": "FinOps", "diff": "Junior"
    },

    # --- SECURITY COMPLIANCE & IDENTITY (10 Questions) ---
    {
        "q": "Difference between Authentication (AuthN) and Authorization (AuthZ)?",
        "ans": "AuthN verifies WHO you are (Login/MFA). AuthZ verifies WHAT you can do (Permissions/Policies).",
        "keys": "Who vs What, Identity vs Permission",
        "topic": "Security", "diff": "Junior"
    },
    {
        "q": "What is OAuth 2.0 vs OIDC (OpenID Connect)?",
        "ans": "OAuth 2.0 is for Authorization (Delegated access, e.g., 'Allow app to access Google Drive'). OIDC is a layer on top of OAuth 2.0 specifically for Authentication (Identity, e.g., 'Log in with Google').",
        "keys": "AuthZ vs AuthN, Access vs Identity, Token types",
        "topic": "Security", "diff": "Senior"
    },
    {
        "q": "What is 'Federated Identity'?",
        "ans": "Allowing users to use their existing corporate identity (Active Directory, Okta, Google) to access AWS/Cloud resources without creating a new IAM user. Uses SAML 2.0 or OIDC.",
        "keys": "SAML, SSO, No IAM users, Centralized management",
        "topic": "Security", "diff": "Mid"
    },
    {
        "q": "Explain 'Envelope Encryption' (KMS).",
        "ans": "KMS encrypts your data key with a master key (CMK). The data key encrypts your actual data. This hierarchy protects the master key and improves performance for large data.",
        "keys": "Data Key vs Master Key, Hierarchy, Performance",
        "topic": "Security", "diff": "Senior"
    },
    {
        "q": "What is a WAF (Web Application Firewall) and what does it block?",
        "ans": "A firewall that inspects HTTP/S traffic at Layer 7. It blocks common attacks like SQL Injection, Cross-Site Scripting (XSS), and bad bots.",
        "keys": "Layer 7, SQLi, XSS, OWASP Top 10",
        "topic": "Security", "diff": "Mid"
    },
    {
        "q": "What is GuardDuty?",
        "ans": "A threat detection service that continuously monitors logs (CloudTrail, VPC Flow Logs, DNS) for malicious activity, such as cryptocurrency mining or unauthorized access attempts.",
        "keys": "Threat detection, Log analysis, ML, Crypto mining",
        "topic": "Security", "diff": "Mid"
    },
    {
        "q": "How do you ensure compliance with HIPAA/SOC2 on AWS?",
        "ans": "Use AWS Artifact to get compliance reports. Enable AWS Config to track configuration history. Encrypt everything at rest and in transit. Enforce Least Privilege.",
        "keys": "Artifact, Config, Encryption, Audit trails",
        "topic": "Compliance", "diff": "Senior"
    },
    {
        "q": "What is 'Secrets Manager' vs 'Parameter Store'?",
        "ans": "Parameter Store is free for standard parameters. Secrets Manager costs money but offers automatic rotation of secrets (changing the DB password automatically) and cross-account access.",
        "keys": "Automatic Rotation, Cost, Simple string vs Secret",
        "topic": "Security", "diff": "Mid"
    },
    {
        "q": "Explain 'Cross-Account Access' via IAM Roles.",
        "ans": "Instead of sharing access keys (unsafe), you create an IAM Role in Account B that trusts Account A. A user in Account A 'assumes' the role to perform actions in Account B securely.",
        "keys": "AssumeRole, Trust Policy, No keys shared",
        "topic": "Security", "diff": "Senior"
    },
    {
        "q": "What is the purpose of a 'Service Control Policy' (SCP)?",
        "ans": "SCPs are organization-level policies (AWS Organizations). They set the maximum available permissions for an account. Even if an Admin in a child account has 'Allow *', the SCP can block specific actions (e.g., 'Deny turning off CloudTrail').",
        "keys": "Organization level, Guardrails, Limit permissions, Root control",
        "topic": "Security", "diff": "Senior"
    }
]

# 3. Batch Prepare
documents = [item["q"] for item in serverless_finops_batch]
ids = [f"q_fin_{i}" for i in range(len(serverless_finops_batch))]
metadatas = [{
    "role": "Cloud Engineer",
    "topic": item["topic"],
    "difficulty": item["diff"],
    "ideal_answer": item["ans"],
    "keywords": item["keys"]
} for item in serverless_finops_batch]

# 4. Insert
print(f"Appending {len(serverless_finops_batch)} FinOps/Serverless questions...")
collection.add(
    documents=documents,
    metadatas=metadatas,
    ids=ids
)

print(f"Done! Database Total: {collection.count()}")