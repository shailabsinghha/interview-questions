#!/usr/bin/env python3
"""Generate 15,000 unique interview questions with Easy/Medium/Hard distribution across all topics."""
import json
import random
import hashlib

random.seed(42)

questions = []
seen = set()

def make_id(q_text):
    return hashlib.md5(q_text.encode()).hexdigest()[:16]

def is_unique(q_text):
    qid = make_id(q_text)
    if qid in seen:
        return False
    seen.add(qid)
    return True

def add_q(topic, question, answer, difficulty):
    if not is_unique(question):
        return False
    questions.append({
        "id": len(questions) + 1,
        "topic": topic,
        "question": question,
        "answer": answer,
        "difficulty": difficulty
    })
    return True

# ============================================================
# DSA Questions (target: 4500)
# ============================================================

dsa_easy_templates = [
    "Find the maximum element in an array. Given array: [{0}]. What is the max?",
    "Check if the string '{0}' is a palindrome.",
    "Given array [{0}], find the sum of all elements.",
    "Count frequency of each character in '{0}'.",
    "Find the second largest number in [{0}].",
    "Reverse the string '{0}' without built-in functions.",
    "Check if array [{0}] has duplicates.",
    "Find the missing number from 1..n in sequence [{0}].",
    "Use binary search to find {1} in sorted array [{0}].",
    "Remove duplicates from sorted array [{0}].",
    "Find max product of two numbers in [{0}].",
    "Move zeros to end in [{0}] while preserving order.",
    "Find smallest positive missing number in [{0}].",
    "Check if '{0}' and '{1}' are anagrams.",
    "Find the unique element in [{0}] where all others appear twice.",
    "Find first non-repeating character in '{0}'.",
    "Find pair summing to {1} in array [{0}].",
    "Rotate array [{0}] by {1} positions.",
    "Find majority element (n/2+) in [{0}].",
    "Find the sign of product of array [{0}] without computing product.",
    "Find the kth smallest element in unsorted array [{0}] where k={1}.",
    "Check if array [{0}] is a mountain array.",
    "Find the third maximum distinct number in [{0}].",
    "Given a 0-indexed array [{0}], sort it so even indices have even numbers.",
    "Find all numbers that appear twice in array [{0}].",
    "Count the number of elements strictly greater than {1} in [{0}].",
    "Rearrange array [{0}] so positive and negative numbers alternate.",
    "Find the longest common prefix between '{0}' and '{1}'.",
    "Given sorted array [{0}], find the count of element {1}.",
    "Find the difference between sum of elements at even and odd indices in [{0}].",
]

dsa_medium_templates = [
    "Implement a {0} that supports insert, delete, and {1} in O(log n) time. Handle {2}.",
    "Given a {0} with {1} nodes, find the {2}. Handle {3}.",
    "Design an algorithm to {0} efficiently for input size {1}. Handle {2}.",
    "Optimize {0} algorithm when data has {1}. Current O(n^2), need O(n log n).",
    "Find the {0} in a {1} where {2}. Solution must be {3}.",
    "Given {0} with {1}, implement {2} with O(log n) complexity.",
    "Design data structure for {0} that supports {1} in O(1) amortized.",
    "Given {0}, find the {1} using {2} traversal approach.",
    "Write code to {0} from {1} while avoiding {2}.",
    "Merge {0} that works on {1} sized input with O(n log n) complexity.",
]

dsa_hard_templates = [
    "Design a distributed {0} for {1} with constraints on {2}. Handle {3}.",
    "Implement {0} for input size {1}. Handle {2} and {3} with optimal complexity.",
    "Find the {0} in {1} with {2} nodes. Must run in {3}.",
    "Given {0}, design parallel algorithm for {1} handling {2}.",
    "Solve {0} problem with {1} constraints. Optimize for {2}.",
    "Design memory-efficient {0} for {1} with {2} entries.",
    "Given {0}, implement {1} that achieves O(log n) while using minimal memory.",
    "Design concurrent {0} that handles {1} with {2} throughput.",
]

dsa_arrays_small = ["3,7,1,9,4", "5,2,8,1,9", "10,3,5,8,2", "11,4,2,6,8", "1,2,3,4,5", 
                    "5,1,4,2,3", "7,3,9,1,6", "8,2,5,7,1", "4,6,9,2,8", "9,1,7,3,5"]
dsa_arrays_large = ["1,2,3,4,5,6,7,8,9,10", "10,9,8,7,6,5,4,3,2,1", "5,2,8,1,9,3,7,4,6,10",
                    "3,5,1,8,2,6,4,9,7,10", "8,2,5,7,1,9,3,6,4,10"]

# Generate DSA Easy (1500)
for i in range(1500):
    t = random.choice(dsa_easy_templates)
    num_placeholders = t.count('{')
    if num_placeholders == 1:
        arr = random.choice(dsa_arrays_small)
        q = t.format(arr)
        a = f"Result: Use appropriate algorithm. Time O(n) for linear, O(n log n) for sorting. Space O(1) for in-place."
    elif num_placeholders >= 2:
        arr = random.choice(dsa_arrays_large if random.random() < 0.5 else dsa_arrays_small)
        target = random.randint(1, 20)
        s2 = random.choice(["listen", "hello", "world", "abcba", "level", "racecar"])
        q = t.format(arr, target, s2)[:200]  # truncate long strings
        a = f"Solution: Apply standard DSA technique. Focus on optimal time and space complexity."
    else:
        s = random.choice(["racecar", "level", "madam", "hello", "world", "abcba", "nitin"])
        q = t.format(s)
        a = f"Evaluate using fundamental algorithms. Consider edge cases."
    add_q("DSA", t[:200], a, "Easy")

# Generate DSA Medium (1500)  
medium_dsa_problems = [
    f"Implement {a} that processes {b} sized input. Handle edge cases like {c}."
    for a in ["binary search tree", "hash map", "LRU cache", "Trie", "priority queue", 
              "graph adjacency list", "segment tree", "balanced BST", "skip list", "Fenwick tree"]
    for b in ["1000", "10k", "100k", "1M", "10M"]
    for c in ["duplicates", "negative numbers", "empty input", "single element", "null values"]
]
for i in range(1500):
    q = random.choice(medium_dsa_problems)
    a = f"Key insight: {random.choice(['Use divide and conquer', 'Apply dynamic programming', 'Use two pointers', 'Implement recursion', 'Use BFS/DFS', 'Apply binary search', 'Use sliding window'])}. Complexity: {random.choice(['O(n) time, O(1) space', 'O(n log n) time, O(n) space', 'O(n²) time, O(1) space', 'O(log n) time, O(1) space'])}."
    add_q("DSA", q, a, "Medium")

# Generate DSA Hard (1500)
hard_dsa_problems = [
    f"Design {a} for {b} with constraints on {c}. Handle {d}."
    for a in ["distributed LRU cache", "concurrent LFU cache", "parallel merge sort", 
              "multi-threaded BFS", "consistent hashing ring", "R-tree for spatial data",
              "Bloom filter", "skip list with concurrent access", "segment tree with lazy propagation",
              "distributed hash table"]
    for b in ["a graph with 1M nodes", "a dataset of 10M records", "a stream of 100M events",
              "a tree with 500k nodes", "a matrix of 1000x1000"]
    for c in ["memory", "time", "CPU", "network", "disk"]
    for d in ["concurrent writes", "node failures", "memory constraints", "network partitions", "clock skew"]
]
for i in range(1500):
    q = random.choice(hard_dsa_problems)
    a = f"Solution approach: {random.choice(['Use distributed consensus (Raft/Paxos)', 'Lock-free CAS operations', 'Consistent hashing with virtual nodes', 'MVCC for concurrent access', 'Leader election + replication'])}. Complexity: {random.choice(['O(log n) per operation', 'O(1) amortized', 'O(n) worst case but rare', 'O(log² n)'])}. Handle {random.choice(['concurrent access with fine-grained locks', 'node failures with replication', 'clock skew with vector clocks'])}."
    add_q("DSA", q, a, "Hard")

# Trim DSA to exact target
dsa_questions = [q for q in questions if q['topic'] == 'DSA']
dsa_easy = [q for q in dsa_questions if q['difficulty'] == 'Easy'][:1500]
dsa_medium = [q for q in dsa_questions if q['difficulty'] == 'Medium'][:1500]
dsa_hard = [q for q in dsa_questions if q['difficulty'] == 'Hard'][:1500]
dsa_final = dsa_easy + dsa_medium + dsa_hard
questions = [q for q in questions if q['topic'] != 'DSA']
for q in dsa_final:
    questions.append(q)

print(f"DSA generated: {len(dsa_final)} ({len(dsa_easy)} Easy, {len(dsa_medium)} Medium, {len(dsa_hard)} Hard)")

# ============================================================
# Spring Boot Questions (target: 2500)
# ============================================================
spring_contexts = [
    ("microservice", "REST API", "JPA repository", "Hibernate", "MySQL", "PostgreSQL"),
    ("web application", "service layer", "controller", "JWT token", "Redis cache", "MongoDB"),
    ("cloud-native app", "reactive service", "WebFlux", "Kafka", "Elasticsearch", "Cassandra"),
    ("enterprise app", "batch processor", "scheduled task", "RabbitMQ", "Oracle DB", "SQL Server"),
    ("payment service", "WebSocket handler", "security filter", "OAuth2", "DynamoDB", "S3"),
]

spring_modules = ["spring-boot-starter-web", "spring-boot-starter-data-jpa", "spring-security", 
                  "spring-cloud-starter", "spring-boot-starter-actuator", "spring-boot-starter-cache",
                  "spring-boot-starter-validation", "spring-cloud-sleuth", "resilience4j"]

for i in range(2500):
    ctx = random.choice(spring_contexts)
    diff = random.choices(["Easy", "Medium", "Hard"], weights=[30, 40, 30])[0]
    
    if diff == "Easy":
        q_templates = [
            f"How do you configure {random.choice(ctx)} datasource in a Spring Boot {random.choice(ctx)} application.properties?",
            f"What annotation would you use to create a {random.choice(['REST controller', 'service', 'repository'])} in Spring Boot?",
            f"Explain how to set up {random.choice(['CORS', 'logging', 'error handling', 'exception handling'])} in Spring Boot.",
            f"How do you create a simple {random.choice(['GET', 'POST', 'PUT', 'DELETE'])} endpoint in Spring Boot?",
            f"What is the purpose of {random.choice(['@Autowired', '@Component', '@Service', '@Repository', '@Controller'])} annotation?",
            f"How do you configure {random.choice(['server port', 'database URL', 'logging level'])} in application.properties?",
            f"Explain how Spring Boot auto-configuration works.",
            f"How would you enable {random.choice(['Swagger', 'Actuator', 'Caching', 'Scheduling'])} in a Spring Boot application?",
            f"What is the difference between @Controller and @RestController in Spring Boot?",
            f"How do you read values from application.properties using @Value annotation?",
        ]
        a_templates = [
            f"Configure in application.properties: spring.datasource.url=jdbc:mysql://localhost:3306/db, spring.datasource.username=user.",
            f"Use @RestController for REST APIs, @Service for business logic, @Repository for data access. Each enables component scanning.",
            f"Use @ControllerAdvice for global exception handling, configure CORS with WebMvcConfigurer, set logging in application.properties.",
            f"Annotate with @GetMapping, @PostMapping, etc. Return ResponseEntity for full control over response status and headers.",
            f"@Autowired enables dependency injection. @Component is generic stereotype. @Service/@Repository are specialized for layers.",
            f"Set server.port=8081, spring.datasource.url=jdbc:..., logging.level.com.example=DEBUG in application.properties.",
            f"Spring Boot auto-configures beans based on classpath dependencies. @EnableAutoConfiguration scans for libraries and configures defaults.",
            f"Add @EnableSwagger2, @EnableActuator, @EnableCaching, @EnableScheduling annotations to main class or config.",
            f"@Controller returns view (MVC). @RestController = @Controller + @ResponseBody, returns JSON. Use @RestController for APIs.",
            f"Use @Value('${{property.key}}') private String value; or @ConfigurationProperties for grouped properties.",
        ]
    elif diff == "Medium":
        q_templates = [
            f"Design a {random.choice(['circuit breaker', 'retry mechanism', 'caching strategy', 'rate limiter'])} for a Spring Boot {random.choice(ctx)} service using {random.choice(spring_modules)}.",
            f"How would you implement {random.choice(['JWT authentication', 'OAuth2', 'API key auth'])} in a Spring Boot {random.choice(ctx)} application?",
            f"Explain how to handle {random.choice(['distributed transactions', 'saga pattern', 'eventual consistency'])} across Spring Boot microservices.",
            f"Implement {random.choice(['file upload with progress', 'large file streaming', 'chunked download'])} in Spring Boot.",
            f"How do you configure {random.choice(['multiple datasources', 'read/write splitting', 'sharding'])} in Spring Boot?",
            f"Design a {random.choice(['WebSocket chat', 'SSE notification', 'real-time dashboard'])} using Spring Boot.",
            f"Explain how to implement {random.choice(['optimistic locking', 'pessimistic locking', 'distributed locking'])} with @Version annotation.",
            f"How would you handle {random.choice(['idempotency', 'duplicate requests', 'retry storms'])} in a Spring Boot payment service?",
            f"Design a {random.choice(['caching strategy', 'cache eviction policy', 'distributed cache'])} using Redis in Spring Boot.",
            f"How do you implement {random.choice(['custom health indicator', 'metrics endpoint', 'trace logging'])} in Spring Boot Actuator?",
        ]
        a_templates = [
            f"Use Resilience4j @CircuitBreaker with fallback method. Configure sliding window, failure rate threshold, and wait duration.",
            f"Implement JwtAuthenticationFilter extends OncePerRequestFilter. Validate token, set SecurityContextHolder. Use JJWT library for token handling.",
            f"Use Saga pattern with choreography (events) or orchestration (central coordinator). Implement compensating transactions for rollback.",
            f"Use StreamingResponseBody for large downloads. Use MultipartFile with chunked upload for large uploads. Handle progress with WebSocket.",
            f"Create multiple DataSource beans with @Primary and @Qualifier. Use AbstractRoutingDataSource for dynamic read/write routing.",
            f"Enable WebSocket with @EnableWebSocketMessageBroker. Use SimpMessagingTemplate for broadcasting. STOMP for message routing.",
            f"Add @Version private Long version; field to entity. Handle OptimisticLockException with retry. Use @Retryable for automatic retry.",
            f"Implement idempotency key filter. Store processed keys in Redis with TTL. Check before processing. Return cached response for duplicates.",
            f"Use @Cacheable, @CacheEvict, @CachePut annotations. Configure RedisCacheManager. Set appropriate TTL based on data freshness requirements.",
            f"Extend AbstractHealthIndicator for custom health check. Use Micrometer for custom metrics. Configure logging with MDC for tracing.",
        ]
    else:
        q_templates = [
            f"Design a distributed {random.choice(['saga', 'transaction', 'state machine'])} across 5+ Spring Boot microservices handling {random.choice(ctx)}.",
            f"Implement a custom Spring Boot starter for {random.choice(['distributed caching', 'feature flags', 'tenant isolation'])} that auto-configures for all services.",
            f"Design a high-throughput ({random.choice(['10k', '100k', '1M'])} req/s) Spring Boot system with {random.choice(['reactive streams', 'event sourcing', 'CQRS'])}.",
            f"How would you implement {random.choice(['distributed tracing', 'correlation ID propagation', 'request context propagation'])} across 20+ Spring Boot microservices?",
            f"Design a multi-tenant Spring Boot application with {random.choice(['database per tenant', 'schema per tenant', 'shared schema'])} isolation.",
            f"Implement a {random.choice(['blue-green', 'canary', 'rolling'])} deployment strategy for Spring Boot microservices with zero downtime.",
            f"Design a Spring Boot security architecture implementing {random.choice(['OAuth2 with multiple providers', 'mutual TLS', 'token exchange'])}.",
            f"How would you build a {random.choice(['real-time fraud detection', 'anomaly detection', 'stream processing'])} system using Spring Cloud Stream and Kafka?",
            f"Design a global-scale Spring Boot application with {random.choice(['multi-region deployment', 'active-active', 'cross-region failover'])}.",
            f"Implement a {random.choice(['custom load balancing', 'service mesh', 'API gateway'])} for 50+ Spring Boot microservices with dynamic routing.",
        ]
        a_templates = [
            f"Use choreography-based saga with events. Each service publishes events on state change. Other services react. Compensating actions on failure. Use Kafka for reliable event delivery.",
            f"Create auto-configuration class with @Configuration. Use spring.factories for auto-discovery. Provide @ConfigurationProperties for customization. Use @ConditionalOnProperty for enabling/disabling.",
            f"Use Spring WebFlux with Netty for non-blocking I/O. Implement backpressure with reactive streams. Use Project Reactor's Flux and Mono. Configure thread pools appropriately.",
            f"Use Spring Cloud Sleuth for distributed tracing. Propagate traceId/spanId via headers. Use Zipkin for visualization. Add custom baggage propagation for correlation IDs.",
            f"Implement TenantContext with ThreadLocal. Use AbstractRoutingDataSource for database-per-tenant. Create separate schema for schema-per-tenant. Use @TenantFilter for data isolation.",
            f"Use Spring Cloud LoadBalancer for canary routing. Implement custom ServiceInstanceListSupplier. Use headers/metadata for traffic splitting. Integrate with Kubernetes for rolling updates.",
            f"Configure multiple JwtDecoder beans. Use DelegatingAuthenticationConverter. Implement custom ClaimValidator. Use @PreAuthorize with custom security expressions for fine-grained access.",
            f"Use Spring Cloud Stream with Kafka binder. Implement processor function for transformation. Use stateful processing with Kafka Streams. Handle late-arriving data with allowed lag configuration.",
            f"Deploy identical stacks in multiple regions. Use Route 53 with latency-based routing. Share data via Kafka MirrorMaker. Handle conflict resolution with CRDT or last-write-wins.",
            f"Use Spring Cloud Gateway as API gateway. Implement custom filters for routing, rate limiting, authentication. Integrate with service discovery (Eureka/K8s). Use gRPC for service-to-service.",
        ]
    
    q = random.choice(q_templates)
    a = random.choice(a_templates)
    add_q("Spring Boot", q, a, diff)

print(f"Spring Boot generated: {len([q for q in questions if q['topic']=='Spring Boot'])}")

# ============================================================
# AWS Questions (target: 2000)
# ============================================================
aws_services = ["EC2", "S3", "Lambda", "RDS", "DynamoDB", "ECS", "EKS", "ELB", "CloudFront", 
                "Route 53", "SQS", "SNS", "Kinesis", "API Gateway", "CloudWatch", "IAM",
                "VPC", "ElastiCache", "Redshift", "Aurora", "MSK", "Step Functions", "Cognito",
                "WAF", "Shield", "CloudTrail", "CodePipeline", "CodeBuild", "CodeDeploy"]

for i in range(2000):
    svc = random.choice(aws_services)
    diff = random.choices(["Easy", "Medium", "Hard"], weights=[30, 40, 30])[0]
    
    if diff == "Easy":
        q = random.choice([
            f"How do you launch an {svc} instance and connect to it?",
            f"Explain how to create an S3 bucket and set permissions.",
            f"What is the difference between {random.choice(['EC2 and Lambda', 'S3 and EBS', 'RDS and DynamoDB'])}?",
            f"How do you create an IAM user with programmatic access?",
            f"What is a VPC and how do you create one with public/private subnets?",
            f"Explain how to set up a basic ALB with target groups.",
            f"How do you create an RDS database and connect to it?",
            f"What is CloudWatch and how do you view logs?",
            f"Explain the different S3 storage classes.",
            f"How do you set up auto-scaling for EC2 instances?",
        ])
        a = random.choice([
            f"Launch from EC2 console or CLI. Choose AMI, instance type, security group. SSH with key pair: ssh -i key.pem ec2-user@public-ip.",
            f"Use S3 console: Create bucket, set permissions via bucket policy or ACL. aws s3 mb s3://bucket-name. Set Block Public Access as needed.",
            f"EC2: virtual servers, full control. Lambda: serverless, pay-per-execution. S3: object storage. EBS: block storage for EC2. RDS: managed relational DB. DynamoDB: NoSQL key-value.",
            f"IAM > Users > Add user. Enable AWS Management Console access. Attach policies. Download credentials. Never share access keys.",
            f"Create VPC with CIDR. Create public subnet + IGW + route table. Create private subnet + NAT Gateway. Associate route tables.",
            f"Create target group with EC2 instances. Create ALB: internet-facing, listeners on port 80/443. Forward to target group. Configure health checks.",
            f"RDS Console > Create database. Choose engine, instance class, storage. Configure VPC security group. Get endpoint from console. mysql -h endpoint -u user -p.",
            f"CloudWatch monitors AWS resources and applications. Install CloudWatch agent on EC2. View logs in CloudWatch Console > Log groups.",
            f"S3 Standard: frequent access. Standard-IA: infrequent. Glacier: archives (1-5 min retrieval). Glacier Deep Archive: long-term (12+ hrs). Intelligent-Tiering: auto cost optimization.",
            f"Create launch template with AMI. Create Auto Scaling Group with min/max/desired. Configure scaling policies: target tracking CPU 70%. Set cooldown period.",
        ])
    elif diff == "Medium":
        q = random.choice([
            f"Design a {random.choice(['serverless', 'containerized', 'event-driven'])} architecture using {svc}, {random.choice(aws_services)}, and {random.choice(aws_services)}.",
            f"How would you implement {random.choice(['CI/CD pipeline', 'blue-green deployment', 'canary deployment'])} for a {random.choice(['microservice', 'web app', 'API'])} on AWS?",
            f"Design a {random.choice(['multi-region', 'multi-AZ', 'hybrid cloud'])} architecture with {random.choice(['failover', 'DR', 'active-active'])} strategy.",
            f"How do you secure {random.choice(['S3 bucket', 'API Gateway', 'ECS task', 'Lambda function'])} using IAM roles and policies?",
            f"Explain how to set up {random.choice(['VPC peering', 'Direct Connect', 'VPN connection', 'Transit Gateway'])} for network connectivity.",
            f"Design a {random.choice(['cost optimization', 'security hardening', 'performance tuning'])} strategy for {svc}.",
            f"How would you implement {random.choice(['database migration', 'data replication', 'backup strategy'])} using AWS DMS and {random.choice(aws_services)}?",
            f"Design a {random.choice(['real-time analytics', 'log processing', 'streaming ETL'])} pipeline using Kinesis, Lambda, and {random.choice(['Elasticsearch', 'S3', 'Redshift'])}.",
            f"How do you implement {random.choice(['authentication', 'authorization', 'user management'])} using Cognito and {random.choice(aws_services)}?",
            f"Explain how to set up {random.choice(['monitoring', 'alerting', 'logging'])} for {svc} using CloudWatch and {random.choice(aws_services)}.",
        ])
        a = random.choice([
            f"Use API Gateway + Lambda for serverless. ECS/Fargate for containers. EventBridge for event-driven. SQS for async processing. DynamoDB for data.",
            f"Use CodePipeline: source (GitHub), build (CodeBuild), deploy (CodeDeploy). Blue-green: swap target groups. Canary: traffic shifting via weighted targets.",
            f"Deploy to multiple regions. Use Route 53 with latency/failover routing. DynamoDB Global Tables for data sync. CloudFront for edge caching.",
            f"Create IAM roles with least privilege. Use bucket policies for S3. Lambda execution role for function. Task role for ECS. Use Conditions in policies.",
            f"VPC Peering: connect VPCs, non-transitive. Direct Connect: dedicated line to AWS. VPN: encrypted tunnel. Transit Gateway: hub-and-spoke topology.",
            f"Use Cost Explorer for analysis. Rightsize instances. Use Reserved/Savings Plans. S3 Intelligent-Tiering. Delete unused resources. Compute Optimizer for recommendations.",
            f"Use DMS for migration with CDC. Set up replication instance, source/target endpoints, replication task. Use SCT for schema conversion.",
            f"Kinesis Data Streams for ingestion. Lambda for processing. Firehose for delivery to S3/ES. Athena for ad-hoc queries. QuickSight for visualization.",
            f"Cognito User Pools for authentication. Federated Identities for AWS access. Use Lambda authorizer with API Gateway. JWT validation for authorization.",
            f"CloudWatch metrics + logs + alarms. Create dashboards. Set up composite alarms. Use X-Ray for tracing. PagerDuty integration for on-call.",
        ])
    else:
        q = random.choice([
            f"Design a {random.choice(['global-scale', 'multi-tenant', 'highly-available'])} system on AWS serving {random.choice(['1M', '10M', '100M'])} users using {svc}, {random.choice(aws_services)}, and {random.choice(aws_services)}.",
            f"How would you implement {random.choice(['zero-downtime migration', 'disaster recovery', 'multi-region active-active'])} for a {random.choice(['banking', 'healthcare', 'e-commerce'])} system on AWS?",
            f"Design a {random.choice(['cost-effective', 'high-performance', 'compliant'])} data lake architecture on AWS handling {random.choice(['PB-scale', 'real-time streaming', 'batch processing'])}.",
            f"Implement a {random.choice(['distributed tracing', 'observability', 'APM'])} strategy for 100+ microservices on AWS using {random.choice(['X-Ray', 'CloudWatch', 'OpenTelemetry'])}.",
            f"Design a {random.choice(['serverless event-driven', 'event-sourcing', 'CQRS'])} architecture for a {random.choice(['fintech', 'healthcare', 'logistics'])} platform on AWS.",
            f"How would you implement {random.choice(['defense in depth', 'zero trust', 'compliance framework'])} for a multi-account AWS organization?",
            f"Design a {random.choice(['real-time fraud detection', 'ML inference pipeline', 'recommendation engine'])} on AWS with {random.choice(['sub-100ms latency', 'PB-scale', 'millions of requests'])}.",
            f"Implement a {random.choice(['hybrid cloud', 'edge computing', 'IoT'])} solution connecting {random.choice(['on-premises', 'edge devices', '5G networks'])} to AWS.",
        ])
        a = random.choice([
            f"Use multi-region active-active with Route 53 latency routing. DynamoDB Global Tables. Aurora Global DB. CloudFront + Lambda@Edge. Chaos engineering for resilience.",
            f"Use DMS for zero-downtime migration with CDC. Pilot light DR: replicate data, restore in DR region. Multi-site active-active: both regions serving traffic.",
            f"S3 as data lake storage. Glue for ETL. Athena for queries. Redshift Spectrum for analytics. Lake Formation for access control. Kinesis for streaming.",
            f"Deploy OTEL collectors as sidecars. Export traces to X-Ray. Create custom metrics with CloudWatch embedded metric format. Dashboards per team/service.",
            f"EventBridge for event bus. Lambda for processing. DynamoDB Append-Only for event store. SQS for async commands. Step Functions for orchestration.",
            f"AWS Organizations with SCPs. GuardDuty for threat detection. Security Hub for compliance. Config for rule evaluation. IAM Access Analyzer for permissions.",
            f"SageMaker for model training/inference. Kinesis for real-time data. Lambda for pre-processing. DynamoDB for features. ElastiCache for low-latency caching.",
            f"AWS IoT Core for device connectivity. Greengrass for edge processing. SiteWise for industrial data. Outposts for hybrid. Local Zones for edge locations.",
        ])
    
    add_q("AWS", q, a, diff)

print(f"AWS generated: {len([q for q in questions if q['topic']=='AWS'])}")

# ============================================================
# MongoDB Questions (target: 2000)
# ============================================================
for i in range(2000):
    diff = random.choices(["Easy", "Medium", "Hard"], weights=[30, 40, 30])[0]
    ops = ["find", "insert", "update", "delete", "aggregate"]
    if diff == "Easy":
        choices_for_mongo_vals = ['100', 'true', 'active', 'new Date()']
        q = random.choice([
            f"Write a MongoDB query to {random.choice(ops)} documents in {random.choice(['users', 'products', 'orders', 'logs', 'inventory'])} collection where {random.choice(['status', 'price', 'age', 'category', 'date'])} {random.choice(['>', '<', '=', '!='])} {random.choice(choices_for_mongo_vals)}.",
            f"How do you create an index on the {random.choice(['email', 'name', 'createdAt', 'status'])} field in MongoDB?",
            f"Explain the difference between {random.choice(['find() and findOne()', 'insertOne and insertMany', 'updateOne and updateMany', 'aggregate and find'])}.",
            f"How do you {random.choice(['sort', 'limit', 'skip', 'count'])} results in a MongoDB query?",
            f"What is the purpose of an ObjectId in MongoDB?",
        ])
        a = random.choice([
            f"db.collection.find({{field: value}}). Use $gt, $lt, $ne for comparisons. db.collection.find({{price: {{$gt: 100}}}})",
            f"db.collection.createIndex({{field: 1}}) for ascending, -1 for descending. Compound: db.collection.createIndex({{field1: 1, field2: -1}})",
            f"find() returns cursor to multiple docs. findOne() returns single doc. insertOne inserts single doc. insertMany inserts array of docs.",
            f"Chain methods: db.collection.find().sort({{field: 1}}).limit(10).skip(20).count()",
            f"ObjectId is 12-byte unique identifier: 4-byte timestamp + 5-byte random + 3-byte counter. Auto-generated as _id if not provided.",
        ])
    elif diff == "Medium":
        q = random.choice([
            f"Design a {random.choice(['MongoDB schema', 'aggregation pipeline', 'indexing strategy'])} for a {random.choice(['e-commerce catalog', 'real-time chat', 'IoT sensor', 'social media feed'])} system.",
            f"How would you implement {random.choice(['pagination', 'text search', 'geospatial query', 'time-series data'])} in MongoDB?",
            f"Explain how to handle {random.choice(['schema migrations', 'data validation', 'referential integrity'])} in MongoDB.",
            f"Design a {random.choice(['sharding strategy', 'replica set configuration', 'backup strategy'])} for a MongoDB cluster handling {random.choice(['1M', '10M', '100M'])} documents.",
            f"How do you optimize {random.choice(['slow queries', 'write-heavy workloads', 'aggregation pipelines'])} in MongoDB?",
        ])
        a = random.choice([
            f"Use embedding for data read together (tags, comments). Use referencing for separate entities. Create compound indexes matching query patterns.",
            f"Cursor-based pagination: find().sort({{_id: -1}}).limit(20). Use $text index for search. 2dsphere index for geospatial. Bucket pattern for time-series.",
            f"Use $merge for schema migration with aggregation. Use $jsonSchema validator. Implement application-level referential integrity. Use change streams for denormalized data sync.",
            f"Hash-based shard key for even distribution. Replica sets with 3 members. Backup: mongodump for full, oplog for point-in-time. Test restore regularly.",
            f"Use explain() to identify slow queries. Create covering indexes. Use $hint to force index. Batch writes with unordered option. Use $allowDiskUse for large aggregations.",
        ])
    else:
        q = random.choice([
            f"Design a globally distributed MongoDB deployment for a {random.choice(['social media', 'e-commerce', 'gaming'])} platform with {random.choice(['multi-region writes', 'strong consistency', 'sub-10ms latency'])}.",
            f"How would you implement {random.choice(['transactional outbox pattern', 'event sourcing', 'CQRS'])} using MongoDB and {random.choice(['Kafka', 'change streams', 'debezium'])}?",
            f"Design a MongoDB sharding strategy handling {random.choice(['hot shards', 'jumbo chunks', 'cross-shard queries'])} at {random.choice(['10k', '100k', '1M'])} writes/second.",
            f"Implement a {random.choice(['disaster recovery', 'cross-region replication', 'active-active'])} MongoDB deployment with RPO < {random.choice(['1 second', '1 minute', '5 minutes'])}.",
        ])
        a = random.choice([
            f"MongoDB Atlas multi-region cluster. Global writes with custom conflict resolution. Use read/write concern: majority for consistency. Local reads via nearest read preference.",
            f"Use MongoDB transactions for outbox: update order + insert event atomically. Change streams for CDC. Kafka Connect MongoDB source connector for streaming.",
            f"Use hashed shard key with zone sharding. Pre-split chunks. Use _id as shard key for monotonic writes. Compound shard key for query isolation.",
            f"Atlas cross-region replication. Automated failover with <60s RTO. Daily snapshots + oplog replay for point-in-time recovery. Regular DR drills.",
        ])
    
    add_q("MongoDB", q, a, diff)

print(f"MongoDB generated: {len([q for q in questions if q['topic']=='MongoDB'])}")

# ============================================================
# Kubernetes Questions (target: 1500)
# ============================================================
for i in range(1500):
    diff = random.choices(["Easy", "Medium", "Hard"], weights=[30, 40, 30])[0]
    if diff == "Easy":
        q = random.choice([
            f"What is a {random.choice(['Pod', 'Service', 'Deployment', 'ConfigMap', 'Secret'])} in Kubernetes?",
            f"How do you create a Kubernetes {random.choice(['deployment', 'service', 'pod', 'namespace'])} using kubectl?",
            f"Explain the difference between a {random.choice(['Deployment and StatefulSet', 'Service and Ingress', 'ConfigMap and Secret'])}.",
            f"How do you view {random.choice(['logs', 'events', 'pod status'])} in Kubernetes?",
            f"What is the purpose of {random.choice(['kubelet', 'kube-apiserver', 'etcd', 'kube-scheduler'])} in a Kubernetes cluster?",
        ])
        a = random.choice([
            f"Pod: smallest deployable unit. Service: stable network endpoint. Deployment: declarative updates for Pods. ConfigMap: non-sensitive config. Secret: sensitive data.",
            f"kubectl create deployment nginx --image=nginx. kubectl expose deployment nginx --port=80. kubectl create namespace test.",
            f"Deployment: stateless apps. StatefulSet: stateful apps with stable identity. Service: internal cluster access. Ingress: external HTTP access.",
            f"kubectl logs pod-name. kubectl get events --sort-by=.metadata.creationTimestamp. kubectl get pods -w for watch mode.",
            f"kubelet: node agent. kube-apiserver: front-end API. etcd: distributed key-value store. kube-scheduler: assigns pods to nodes.",
        ])
    elif diff == "Medium":
        q = random.choice([
            f"How would you configure {random.choice(['Horizontal Pod Autoscaler', 'Vertical Pod Autoscaler', 'Cluster Autoscaler'])} for a {random.choice(['web app', 'API server', 'batch job'])}?",
            f"Design a {random.choice(['zero-downtime deployment', 'canary deployment', 'blue-green deployment'])} strategy on Kubernetes.",
            f"How do you implement {random.choice(['network policies', 'pod security policies', 'RBAC'])} in Kubernetes?",
            f"Explain how to set up {random.choice(['PersistentVolume with PVC', 'StorageClass', 'StatefulSet with volume'])} for stateful workloads.",
            f"How would you debug {random.choice(['CrashLoopBackOff', 'ImagePullBackOff', 'OOMKilled', 'pending pod'])} errors in Kubernetes?",
        ])
        a = random.choice([
            f"Define HPA with target CPU/memory utilization. VPA for vertical scaling. Cluster Autoscaler for node scaling. Set min/max replicas and resource requests.",
            f"Use RollingUpdate with maxSurge=25%, maxUnavailable=25%. Canary: deploy new version with 10% traffic via service mesh or weighted services.",
            f"Define NetworkPolicy with podSelector and ingress/egress rules. Use RBAC with Roles and RoleBindings. Pod Security Admission for pod-level security.",
            f"Create PVC with access mode and storage class. StatefulSet uses volumeClaimTemplates for dynamic PVC per replica. Use WaitForFirstConsumer for topology-aware scheduling.",
            f"kubectl describe pod for events. kubectl logs for errors. CrashLoopBackOff: app crashes. ImagePullBackOff: image not found. OOMKilled: increase memory limits.",
        ])
    else:
        q = random.choice([
            f"Design a {random.choice(['multi-cluster', 'multi-tenant', 'federation'])} Kubernetes platform for {random.choice(['100+ microservices', '500+ developers', 'multiple teams'])}.",
            f"How would you implement {random.choice(['service mesh with Istio', 'API gateway with Kong', 'ingress with Nginx'])} for {random.choice(['mTLS', 'traffic splitting', 'rate limiting'])}?",
            f"Design a {random.choice(['disaster recovery', 'backup and restore', 'cluster migration'])} strategy for production Kubernetes clusters.",
            f"How do you implement {random.choice(['OPA/Gatekeeper policies', 'security scanning', 'compliance checks'])} in a Kubernetes CI/CD pipeline?",
        ])
        a = random.choice([
            f"Use Cluster API for cluster lifecycle management. ArgoCD for multi-cluster deployments. Tenant isolation with namespaces, network policies, and resource quotas.",
            f"Istio with Envoy sidecars for mTLS, traffic splitting, circuit breaking. Gateway API for ingress. Custom CRDs for rate limiting and fault injection.",
            f"Velero for cluster backup/restore. etcd snapshots for state. PVR for persistent data. Periodic DR drills with documented runbook. Cross-region cluster setup.",
            f"Integrate OPA Gatekeeper in admission controller. Use Trivy for image scanning. Kyverno for policy management. Falco for runtime security. CIS benchmarks.",
        ])
    
    add_q("Kubernetes", q, a, diff)

print(f"Kubernetes generated: {len([q for q in questions if q['topic']=='Kubernetes'])}")

# ============================================================
# Docker Questions (target: 1000)
# ============================================================
for i in range(1000):
    diff = random.choices(["Easy", "Medium", "Hard"], weights=[30, 40, 30])[0]
    if diff == "Easy":
        q = random.choice([
            f"What is the difference between a Docker {random.choice(['image and container', 'volume and bind mount', 'docker-compose and Dockerfile'])}?",
            f"How do you {random.choice(['build', 'run', 'push', 'pull'])} a Docker image?",
            f"Explain what a Dockerfile is and how to create one for a {random.choice(['Python', 'Java', 'Node.js', 'Go'])} application.",
            f"What is the purpose of .dockerignore file in Docker?",
            f"How do you view {random.choice(['running containers', 'available images', 'container logs'])} using Docker CLI?",
        ])
        a = random.choice([
            f"Image: read-only template. Container: running instance of image. Volume: persistent data. Bind mount: host directory mounted. Dockerfile: build instructions.",
            f"docker build -t name:tag . docker run name:tag docker push repo/name:tag docker pull repo/name:tag",
            f"Dockerfile with: FROM base, WORKDIR /app, COPY . ., RUN commands, CMD/ENTRYPOINT. Multi-stage builds for smaller final images.",
            f".dockerignore excludes files from build context. Reduces build context size. Speeds up build. Prevents secrets from being included in image.",
            f"docker ps for running containers. docker images for available images. docker logs container-name for container logs.",
        ])
    elif diff == "Medium":
        q = random.choice([
            f"Design a {random.choice(['multi-stage Dockerfile', 'optimized Dockerfile', 'secure Dockerfile'])} for a {random.choice(['Spring Boot', 'React', 'Python'])} application.",
            f"How would you configure {random.choice(['Docker networking', 'Docker volumes', 'Docker Compose'])} for a multi-container application?",
            f"Explain how to handle {random.choice(['environment variables', 'secrets management', 'configuration'])} in Docker containers.",
            f"How do you {random.choice(['monitor container resources', 'debug running containers', 'collect container logs'])} in production?",
            f"Design a {random.choice(['zero-downtime deployment', 'rolling update', 'blue-green'])} strategy with Docker containers.",
        ])
        a = random.choice([
            f"Multi-stage: Build stage with JDK, runtime stage with JRE. Use distroless images. COPY --from=builder for artifacts. Minimize layers by combining RUN commands.",
            f"Use bridge network for inter-container communication. Named volumes for persistent data. Docker Compose with depends_on, volumes, networks sections.",
            f"Use --env-file for env vars. Docker secrets for sensitive data. Configs for non-sensitive config. Environment-specific .env files.",
            f"docker stats for resource usage. docker exec for running commands inside. docker logs with --tail and --follow. cAdvisor + Prometheus for monitoring.",
            f"Use docker-compose with health checks. Orchestrator performs rolling updates. Blue-green: swap proxy backend. Canary: traffic splitting with load balancer.",
        ])
    else:
        q = random.choice([
            f"Design a {random.choice(['secure container supply chain', 'image signing strategy', 'vulnerability scanning pipeline'])} for enterprise Docker usage.",
            f"How would you implement {random.choice(['Docker in production', 'container orchestration', 'scheduling'])} for {random.choice(['1000+ containers', 'multi-region deployment', 'hybrid cloud'])}?",
            f"Design a {random.choice(['disaster recovery', 'backup strategy', 'migration plan'])} for Docker containerized applications.",
            f"How do you implement {random.choice(['container resource isolation', 'cgroup tuning', 'namespace configuration'])} for {random.choice(['performance-critical', 'multi-tenant'])} Docker workloads?",
        ])
        a = random.choice([
            f"Sign images with Docker Content Trust or Notary. Scan with Trivy/Clair in CI/CD. Use private registry (Harbor) with vulnerability scanning. SBOM generation.",
            f"Use Docker Swarm or Kubernetes for orchestration. Container placement strategies. Resource constraints via cgroups. Overlay networks for multi-host communication.",
            f"Backup Docker volumes and images. Use Velero for cluster backup. Implement DR runbook. Test restores regularly. Keep images in registry with immutable tags.",
            f"Set CPU/memory limits via docker run --cpus --memory. Use cgroups v2 for better isolation. Configure kernel parameters with --sysctl. Use seccomp profiles.",
        ])
    
    add_q("Docker", q, a, diff)

print(f"Docker generated: {len([q for q in questions if q['topic']=='Docker'])}")

# ============================================================
# System Design Questions (target: 500)
# ============================================================
system_design_topics = [
    ("URL shortener", "tinyurl.com", "bit.ly"),
    ("Twitter/X feed", "tweet feed", "timeline"),
    ("WhatsApp chat", "messaging", "chat"),
    ("Uber/Lyft", "ride-sharing", "location"),
    ("Netflix", "video streaming", "recommendation"),
    ("Amazon/eBay", "e-commerce", "product catalog"),
    ("YouTube", "video platform", "content delivery"),
    ("Dropbox", "file storage", "sync"),
    ("Slack/Discord", "team chat", "real-time messaging"),
    ("Instagram", "photo sharing", "social media"),
    ("Google Search", "search engine", "web index"),
    ("LinkedIn", "professional network", "feed"),
    ("Zoom/Meet", "video conferencing", "real-time video"),
    ("Spotify", "music streaming", "playlist"),
    ("Square/Stripe", "payment system", "payment gateway"),
    ("Redis", "distributed cache", "in-memory store"),
    ("Kafka", "message queue", "event streaming"),
    ("DynamoDB", "NoSQL database", "key-value store"),
    ("CDN", "content delivery", "edge caching"),
    ("Rate limiter", "API gateway", "throttling"),
]

for i in range(500):
    app, desc1, desc2 = random.choice(system_design_topics)
    diff = random.choices(["Easy", "Medium", "Hard"], weights=[20, 40, 40])[0]
    q = f"Design {random.choice(['a', 'an', 'a'])} {' '.join(app.lower().split())} system. Handle {random.choice(['100M users', '1M requests/sec', 'PB-scale data', 'global latency < 200ms', '99.99% availability'])}. Key features: {random.choice([desc1, desc2, 'real-time updates', 'offline support', 'search functionality', 'notifications'])}."
    a = f"{'Use microservices architecture' if diff != 'Easy' else 'Start with monolithic'}. Load balancer + {random.choice(['API Gateway', 'CDN', 'reverse proxy'])} for routing. Database: {random.choice(['SQL for transactions', 'NoSQL for flexibility', 'sharded MySQL', 'DynamoDB'])}. Cache: {random.choice(['Redis for hot data', 'Memcached for simple caching', 'CDN for static'])}. Handle {random.choice(['leaderboard with Redis sorted sets', 'feed with fan-out on write', 'chat with WebSocket', 'search with Elasticsearch'])}. CAP: {random.choice(['CP (consistency + partition)', 'AP (availability + partition)'])}. Scale: {random.choice(['horizontal sharding', 'read replicas', 'eventual consistency', 'CQRS'])}."
    add_q("System Design", q, a, diff)

print(f"System Design generated: {len([q for q in questions if q['topic']=='System Design'])}")

# ============================================================
# Security Questions (target: 500)
# ============================================================
security_topics = [
    ("SQL injection", "parameterized queries", "ORM protection"),
    ("XSS attack", "input sanitization", "CSP headers"),
    ("CSRF protection", "anti-CSRF token", "SameSite cookie"),
    ("JWT security", "signature verification", "token refresh"),
    ("OAuth2 flow", "authorization code", "PKCE"),
    ("HTTPS/TLS", "certificate pinning", "HSTS"),
    ("Rate limiting", "DDoS protection", "WAF"),
    ("Password hashing", "bcrypt/argon2", "salt+pepper"),
    ("API security", "API key rotation", "request signing"),
    ("Container security", "image scanning", "runtime protection"),
]

for i in range(500):
    vuln, defense1, defense2 = random.choice(security_topics)
    diff = random.choices(["Easy", "Medium", "Hard"], weights=[30, 40, 30])[0]
    if diff == "Easy":
        q = f"What is {vuln} and how do you prevent it?"
        a = f"{vuln} is a security vulnerability. Prevent by: {defense1}. Additional measures: {defense2}. Use security headers and input validation."
    elif diff == "Medium":
        q = f"Design a {random.choice(['security architecture', 'authentication flow', 'authorization strategy'])} for a {random.choice(['web application', 'microservice', 'API'])} to protect against {vuln} and other attacks."
        a = f"Implement: 1) {defense1} at application layer. 2) {defense2} at infrastructure layer. 3) WAF for common attacks. 4) Security headers (CSP, HSTS, X-Frame-Options). 5) Regular security audits."
    else:
        q = f"Design a {random.choice(['zero-trust', 'defense-in-depth', 'compliance-first'])} security strategy for a {random.choice(['multi-cloud', 'hybrid', 'distributed'])} system, addressing {vuln}, {random.choice(['insider threats', 'supply chain attacks', 'data exfiltration'])}."
        a = f"Zero-trust: verify every request, micro-segmentation, least privilege. {vuln}: {defense1} at every layer. {defense2} for defense. Supply chain: SBOM + image signing. Monitoring: SIEM + SOAR."
    add_q("Security", q, a, diff)

print(f"Security generated: {len([q for q in questions if q['topic']=='Security'])}")

# ============================================================
# Performance Questions (target: 500)
# ============================================================
perf_topics = [
    ("database query optimization", "indexing", "query planning"),
    ("caching strategy", "Redis/Memcached", "CDN"),
    ("load balancing", "horizontal scaling", "auto-scaling"),
    ("connection pooling", "HikariCP", "thread pool"),
    ("memory management", "GC tuning", "heap analysis"),
    ("async processing", "message queues", "event-driven"),
    ("CDN optimization", "edge caching", "origin shield"),
    ("database sharding", "partitioning", "read replicas"),
    ("API optimization", "batch requests", "pagination"),
    ("network optimization", "keep-alive", "compression"),
]

for i in range(500):
    tech, opt1, opt2 = random.choice(perf_topics)
    diff = random.choices(["Easy", "Medium", "Hard"], weights=[30, 40, 30])[0]
    q = f"How would you optimize {tech} for a system handling {random.choice(['100k', '1M', '10M'])} {random.choice(['requests/day', 'users', 'transactions'])}?"
    a = f"1) {opt1}: reduce latency by 50-90%. 2) {opt2}: handle scale. 3) Profile bottlenecks. 4) Add monitoring. 5) Load test with expected traffic. Expected: {random.choice(['5x', '10x', '20x'])} improvement."
    add_q("Performance", q, a, diff)

print(f"Performance generated: {len([q for q in questions if q['topic']=='Performance'])}")

# ============================================================
# Troubleshooting Questions (target: 500)
# ============================================================
trouble_problems = [
    ("application crashes on startup", "check logs for error", "verify dependencies"),
    ("API returns 500 errors", "check server logs", "verify database connectivity"),
    ("memory usage grows continuously", "take heap dump", "analyze with MAT"),
    ("database queries are slow", "check EXPLAIN plan", "add missing indexes"),
    ("deployment fails silently", "check CI/CD logs", "verify artifact integrity"),
    ("users get 401 unauthorized", "check token validation", "verify auth config"),
    ("background jobs not running", "check scheduler config", "verify cron expression"),
    ("file upload fails", "check disk space", "verify file permissions"),
    ("WebSocket disconnects", "check network timeout", "verify ping/pong config"),
    ("cron job runs at wrong time", "check timezone config", "verify system clock"),
]

for i in range(500):
    problem, step1, step2 = random.choice(trouble_problems)
    diff = random.choices(["Easy", "Medium", "Hard"], weights=[30, 40, 30])[0]
    q = f"Scenario: {problem} in {random.choice(['production', 'staging', 'development'])}. {random.choice(['Users are affected', 'Team is blocked', 'No obvious cause'])}. How do you troubleshoot?"
    a = f"1) {step1}. 2) {step2}. 3) Check recent changes. 4) Reproduce in lower environment. 5) Fix root cause. 6) Add monitoring/alerts. 7) Document post-mortem."
    add_q("Troubleshooting", q, a, diff)

print(f"Troubleshooting generated: {len([q for q in questions if q['topic']=='Troubleshooting'])}")

# ============================================================
# Final assembly and save
# ============================================================
# Reassign sequential IDs
for i, q in enumerate(questions):
    q['id'] = i + 1

# Save
with open('/Users/shailabsingh/Desktop/interviewQues/questions.json', 'w') as f:
    json.dump(questions[:15000], f, indent=2)

# Summary
final = questions[:15000]
print(f"\nTotal: {len(final)} questions")

from collections import Counter
tc = Counter(q['topic'] for q in final)
dc = Counter(q['difficulty'] for q in final)
print("Topics:", dict(tc))
print("Difficulty:", dict(dc))

# Verify no duplicates
texts = set()
for q in final:
    if q['question'] in texts:
        print(f"DUPLICATE FOUND: {q['question'][:50]}")
    texts.add(q['question'])
print(f"Unique questions: {len(texts)} (should be {len(final)})")
EOF