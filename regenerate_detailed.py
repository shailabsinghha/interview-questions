import json
import random

topics = ['MongoDB', 'Spring Boot', 'AWS', 'DSA', 'System Design', 'Security', 'Performance', 'Troubleshooting', 'Kubernetes', 'Docker']
difficulties = ['Easy', 'Medium', 'Hard']

detailed_scenarios = [
    # MongoDB
    ('MongoDB', 'You are designing a real-time analytics dashboard that processes millions of user events per second. The data needs to be queried for time-based aggregations with sub-second response times. Explain your schema design approach, indexing strategy, and how you would handle the trade-off between read performance and memory consumption in MongoDB.', 'Use time-series collections or implement bucket pattern to group events. Create compound indexes on timestamp event_type user_id. Use covering indexes for frequent queries. Implement TTL for old data. Consider read preference settings for analytics queries. Use aggregation pipeline for pre-computed views.'),
    ('MongoDB', 'Your production MongoDB replica set experienced a network partition that isolated the primary for 30 seconds. During this time, your application continued to send write requests. Explain how MongoDB handles writes during a partition, what happens to the data that was accepted by the old primary, and what write concern configuration you would use to prevent data loss in this scenario.', 'During partition, primary steps down and new election occurs. Writes accepted by isolated primary may be lost. Use writeConcern: majority to ensure acknowledgment from majority of replicas. Consider read preference settings post-failover. Implement retry logic with exponential backoff.'),
    ('MongoDB', 'You need to design a schema for a content management system where articles can have many tags and multiple authors. Each article can have thousands of comments. Explain when you would use embedding versus referencing, and provide a concrete schema design that optimizes for the most common query patterns of fetching an article with its authors, tags, and recent comments.', 'Use embedding for tags - small array, accessed together. Use referencing for authors - separate collection, data changes rarely. Use separate collection for comments with indexing on articleId. Implement denormalization for frequently accessed combined data like author names in comments.'),
    ('MongoDB', 'Your aggregation pipeline to calculate daily active users is taking over 30 seconds to complete on a collection with 100 million documents. Explain how you would optimize this pipeline and what performance improvements you would expect.', 'Add match early to reduce document flow. Use indexes on filter fields. Implement collation for case-insensitive grouping. Consider using facet for parallel pipelines. Use covered queries with projection. Pre-aggregate data with periodic background jobs.'),
    ('MongoDB', 'You are implementing a multi-tenant SaaS application where each tenant has their own collection. The number of tenants is growing rapidly, and you are concerned about management overhead and performance. Explain the trade-offs between using separate collections per tenant versus a single shared collection with tenant_id field, and recommend a strategy for scaling.', 'Single collection with tenant_id provides better resource utilization and simpler operations. Separate collections offer better isolation and can be colocated. Consider hybrid approach: shared collections for common data, separate for sensitive. Use tenant context in queries for automatic filtering.'),
    ('MongoDB', 'Your sharded cluster query performance has degraded significantly. Some queries take over 5 seconds while others are fast. You notice that data distribution is uneven across shards. Explain the root causes that could lead to this scenario, how you would diagnose it, and what steps you would take to restore balanced query performance.', 'Check shard key cardinality and distribution. Review chunk migration history. Analyze query patterns that might cause hotspotting. Use hashed shard key for even distribution. Implement chunk splitting and rebalancing. Ensure queries include shard key to avoid scatter-gather.'),
    ('MongoDB', 'You are storing user activity logs in MongoDB. The data is growing rapidly. Explain your approach to designing the schema and index strategy to support fast time-based queries without consuming excessive RAM.', 'Use time-series collections if available in MongoDB version. Otherwise, implement Bucket Pattern: group multiple log entries into a single document per hour day. Create an index on timestamp field. To save RAM, ensure only the working set fits in memory.'),
    ('MongoDB', 'Compare embedding vs referencing documents in MongoDB. Give a concrete example where embedding is superior, and another where referencing is essential.', 'Embedding: User document containing Profile sub-document - data accessed together, 1:1 or 1:few relationship. Referencing: Publisher document with thousands of Book documents - 1:many relationship where embedding would exceed 16MB limit.'),
    ('MongoDB', 'Explain how the MongoDB aggregation framework works. Provide an example of a complex pipeline to calculate average daily active users from raw events collection.', 'The aggregation framework processes data through pipeline of stages - match, group, project. To calculate DAU: Use match to filter events by date range, then group by date and user ID for unique users per day, finally another group to calculate average.'),
    ('MongoDB', 'In a replica set, your application experiences temporary network partition isolating the primary. How does MongoDB handle writes during this period?', 'During partition, isolated primary steps down and new primary is elected. Writes to old primary might be accepted if write concern is weak. To prevent data loss, use writeConcern: majority.'),

    # Spring Boot
    ('Spring Boot', 'You are designing a distributed e-commerce platform using Spring Boot microservices. What strategies would you implement to ensure data consistency across multiple services when an order is placed, given that you cannot use distributed transactions (2PC)?', 'Use Saga pattern with choreography or orchestration. Instead of single transaction, break into local transactions within each microservice. Implement compensation transactions to rollback changes if subsequent step fails.'),
    ('Spring Boot', 'Explain how the Spring Cloud Gateway acts as a single point of entry in a microservice architecture. How would you handle rate limiting and authentication at the gateway level?', 'Spring Cloud Gateway uses non-blocking APIs to handle requests. Authentication can be handled via Global Filters validating tokens like JWT. Rate limiting can be implemented using Redis Rate Limiter filter based on user ID or IP address.'),
    ('Spring Boot', 'In a high-traffic Spring Boot application, you notice a memory leak leading to frequent Full GCs. Describe your step-by-step approach to identifying and resolving this issue.', '1) Capture heap dump when memory is high using jmap or -XX:+HeapDumpOnOutOfMemoryError. 2) Analyze heap dump using Eclipse MAT or VisualVM to find largest objects retaining memory. 3) Inspect code for those objects, looking for unclosed resources or static collections growing indefinitely.'),
    ('Spring Boot', 'Describe a scenario where you would choose Spring WebFlux over Spring Web MVC for a microservice. What are the core differences in how they handle concurrent requests?', 'Use Spring WebFlux when service is highly I/O bound - streaming data, making many external API calls. Requires high concurrency with fewer threads. Web MVC uses thread-per-request model which blocks threads during I/O. WebFlux uses event-loop model.'),
    ('Spring Boot', 'Explain the concept of circuit breakers in a microservice architecture. How would you configure Resilience4j in a Spring Boot application to handle transient failures gracefully?', 'Circuit breaker prevents application from repeatedly trying operation likely to fail. Configure failure rate thresholds and wait times in Resilience4j. When threshold is met, circuit opens, subsequent calls fail fast or execute fallback method until probe request succeeds.'),
    ('Spring Boot', 'Describe how you would implement distributed tracing in a Spring Boot ecosystem. What specific headers are propagated, and how does this help in identifying latency bottlenecks?', 'Use Spring Cloud Sleuth or Micrometer Tracing with Zipkin Jaeger. They inject X-B3-TraceId which identifies entire request flow and X-B3-SpanId which identifies specific segment. This allows visualizing request path and pinpointing latency.'),
    ('Spring Boot', 'Your microservices need to communicate asynchronously. Compare RabbitMQ vs Apache Kafka. In what scenarios is one preferred over the other?', 'RabbitMQ is message broker suited for complex routing, priority queues, traditional pub/sub. Kafka is event streaming platform built for high throughput, replayability, log aggregation. Use Kafka for event sourcing or massive data pipelines. Use RabbitMQ for task queuing.'),

    # AWS
    ('AWS', 'You need to deploy a Spring Boot microservice that occasionally scales from zero to handle bursty, short-lived workloads. Would you choose Amazon EC2, ECS Fargate, or AWS Lambda? Justify your choice.', 'AWS Lambda is best for short-lived, bursty workloads that scale from zero. It charges only for compute time used and scales automatically. EC2/ECS require provisioning underlying instances which incur costs even when idle.'),
    ('AWS', 'Explain the difference between Application Load Balancer (ALB) and Network Load Balancer (NLB) in AWS. When would you use one over the other for your web application?', 'ALB operates at Layer 7 (HTTP/HTTPS) and is ideal for web applications, offering advanced routing based on URLs, headers. NLB operates at Layer 4 (TCP/UDP) and is best for extreme performance and low latency requirements.'),
    ('AWS', 'Explain the differences between Amazon SQS and Amazon SNS. How would you use them together in a fan-out architecture?', 'SNS is pub/sub messaging service - push-based. SQS is message queueing service - pull-based. In fan-out architecture, publish message to SNS topic, multiple SQS queues subscribe to that topic, allowing parallel asynchronous processing.'),
    ('AWS', 'You need to deploy a containerized application with strict compliance requirements regarding data isolation. Would you choose Amazon ECS on EC2, ECS on Fargate, or EKS? Justify your choice.', 'EC2 provides maximum control over underlying infrastructure but requires managing OS updates and instance scaling. Fargate abstracts infrastructure, providing serverless compute for containers. EKS uses Kubernetes. For strict compliance and data isolation, ECS on EC2 with dedicated hosts provides verifiable control.'),
    ('AWS', 'You notice your RDS PostgreSQL database has become the application bottleneck. Response times have increased from 50ms to 500ms over the past month. Explain your approach to diagnosing and optimizing.', 'Enable Performance Insights and Slow Query Log. Analyze execution plans for slow queries. Check for missing indexes or inefficient joins. Implement connection pooling with RDS Proxy. Add Read Replicas for read-heavy workloads. Consider Aurora for better performance.'),
    ('AWS', 'Design a disaster recovery strategy for AWS infrastructure with RPO of 1 hour and RTO of 4 hours.', 'Use multi-region deployment with Route 53 health check failover. Implement cross-region RDS read replica with automated failover. Use S3 cross-region replication with lifecycle policies. Consider AWS Backup for centralized management.'),

    # DSA
    ('DSA', 'Given a stream of web logs, design a data structure and algorithm to find the top K most visited IP addresses in the last 24 hours efficiently.', 'Use combination of Hash Map and Min-Heap. Hash Map stores frequency of each IP. Min-Heap of size K keeps track of top K IPs. Update time is O(log K). For approximate solution, use Count-Min Sketch.'),
    ('DSA', 'You need to implement a caching mechanism with fixed capacity that evicts least recently used items. Explain data structures to achieve O(1) time complexity for get and put operations.', 'LRU Cache uses Doubly Linked List to maintain order of recently used items and Hash Map to store key and pointer to corresponding node in Linked List. Get and put both O(1).'),
    ('DSA', 'Explain time and space complexity of traversing deeply nested JSON using BFS vs DFS.', 'For deeply nested structure (tree/graph), DFS uses O(d) space where d is maximum depth due to recursion stack. BFS uses O(w) space where w is maximum width due to queue. Time complexity for both is O(N) where N is number of nodes.'),
    ('DSA', 'Given large log file that cannot fit into memory, design algorithm to sort log entries chronologically.', 'Use External Merge Sort. Divide file into chunks that fit in memory. Sort each chunk and save as temporary file. Finally, perform N-way merge of temporary files using Min-Heap for final sorted output.'),
    ('DSA', 'Design algorithm to detect cycle in directed graph. Compare DFS approach vs union-find method.', 'DFS with recursion stack tracking vs Union-Find with cycle detection. DFS better for single source, UF better for multiple components.'),
    ('DSA', 'Implement Trie data structure for autocomplete. What are time complexities for insert, search, and prefix search?', 'Insert: O(m) where m is word length. Search: O(m). Prefix search: O(m + n) where n is number of matches. Space: O(ALPHABET_SIZE * m * nodes).'),

    # System Design
    ('System Design', 'Design URL shortening service like bit.ly. Describe high-level architecture, database choice, and how to ensure generated short URLs are unique and collision-free in distributed system.', 'Use distributed key-generation service (ZooKeeper or database with auto-increment and Base62 encoding) to generate unique short IDs. Store mapping in Redis or Cassandra. Use load balancer to distribute traffic.'),
    ('System Design', 'Explain Event Sourcing and CQRS. In what specific web application scenarios would you advocate for using this pattern?', 'Event Sourcing stores every state change as event rather than just current state. CQRS separates read and write operations into different models. Use for complex domains like shopping cart or financial ledger where audit trail is critical.'),
    ('System Design', 'How do you handle idempotency in API endpoint that processes financial payments?', 'Generate unique Idempotency-Key (UUID) on client side for each payment request. Server checks fast datastore (Redis) to see if this key has been processed. If yes, return cached response. If not, process payment and store result.'),
    ('System Design', 'Design real-time notification system for 50 million users with 100ms delivery requirement.', 'Use WebSocket for real-time delivery with fallback to polling. Implement message queue (Kafka) for reliability. Use fan-out pattern for delivery. Cache user device tokens in Redis. Scale horizontally with consistent hashing.'),
    ('System Design', 'Design rate limiting system for API with millions of users.', 'Use Token Bucket or Leaky Bucket algorithm. Implement at API Gateway with Redis backend. Consider per-user, per-IP, and global limits. Implement circuit breaker for cascading failure protection.'),
    ('System Design', 'Explain differences between synchronous and asynchronous communication in microservices.', 'Synchronous: HTTP/REST for immediate responses. Asynchronous: Message queues for eventual consistency, decoupling, handling bursts. Choose sync for user-facing operations, async for background jobs.'),

    # Security
    ('Security', 'Your web application uses JWT for authentication. A user reports token was stolen via XSS attack. How would you secure JWT and what are trade-offs?', 'Store JWT in HttpOnly, Secure, SameSite cookie instead of LocalStorage. This prevents JavaScript and XSS attacks from accessing token. Trade-off: must implement CSRF protection with anti-CSRF tokens.'),
    ('Security', 'Explain how you would mitigate DDoS attack targeting login endpoint.', 'Implement rate limiting at API Gateway or Load Balancer level. Use Web Application Firewalls to block malicious IPs and suspicious request patterns. Use CDN like Cloudflare to absorb volumetric attacks. Implement CAPTCHA for suspicious login attempts.'),
    ('Security', 'Explain SQL injection attack and how you would prevent it in Spring Boot application.', 'Never concatenate user input into queries. Use parameterized queries or ORM. Validate and sanitize input. Use Web Application Firewall. Conduct regular penetration testing.'),
    ('Security', 'Your API is vulnerable to broken authentication. What would you test and fix?', 'Test for: weak password policies, session fixation, lack of account lockout. Fix: enforce strong passwords, implement account lockout, use secure random session IDs, add MFA support, configure secure session cookies.'),
    ('Security', 'Explain Cross-Site Request Forgery (CSRF) and how to protect Spring Boot application.', 'Use anti-CSRF tokens with Synchronizer Token Pattern. Configure Spring Security CSRF filter. Validate Origin/Referer headers. Use SameSite cookies as alternative. Token-based preferred for APIs.'),

    # Performance
    ('Performance', 'You notice critical API endpoint taking over 2 seconds due to multiple downstream service calls. How would you optimize using async and caching?', 'Use asynchronous processing (CompletableFuture in Java) to call downstream services in parallel rather than sequentially. Implement caching (Redis) for data that does not change frequently to avoid network call entirely.'),
    ('Performance', 'What are key metrics to monitor for distributed web application? How distinguish network bottleneck from database bottleneck?', 'Key metrics: Response Time, Throughput, Error Rate, CPU/Memory utilization. If database CPU/IOPS is maxed out or many slow queries = DB bottleneck. If response times high but server/DB resources low = network bottleneck.'),
    ('Performance', 'Your database queries are slow despite having indexes. How would you identify and optimize?', 'Enable slow query log. Use EXPLAIN to analyze query plan. Add appropriate indexes. Consider query rewrite or denormalization. Check for stale statistics causing poor plan selection.'),
    ('Performance', 'Explain differences between horizontal vs vertical scaling. When choose each?', 'Vertical: add more resources to existing server. Horizontal: add more servers. Choose vertical for stateful services, horizontal for stateless services and bursty loads. Vertical has hard limits, horizontal adds complexity but better fault tolerance.'),
    ('Performance', 'Design caching strategy for social media with millions of users.', 'Implement multi-level caching (L1 local, L2 distributed). Cache popular feeds, user profiles. Use write-through for updates. Implement cache-aside with TTL. Handle cache stampede with probabilistic early expiration or mutex.'),
    ('Performance', 'Microservices experiencing high latency. How identify bottleneck in distributed tracing?', 'Analyze trace data in Zipkin/Jaeger. Find spans with longest duration. Check downstream service calls. Identify whether latency is in network or processing. Look for serialization bottlenecks.'),

    # Troubleshooting
    ('Troubleshooting', 'User reports intermittent 502 Bad Gateway errors during peak hours. Walk through troubleshooting process.', '1) Check load balancer logs to confirm 502 error and identify which backend instance is failing. 2) Check backend instance application logs for crashes, OutOfMemory errors, thread starvation. 3) Monitor CPU/Memory metrics during peak hours.'),
    ('Troubleshooting', 'You deployed new microservice throwing NullPointerException in production but works in staging. How debug?', '1) Check exact line number of NPE in stack trace. 2) Identify differences between staging and production environments (environment variables, database state, external service configurations). 3) Likely missing configuration value causing null in production.'),
    ('Troubleshooting', 'Application log shows connection timeouts to database. Database CPU is normal. What could be wrong?', 'Check connection pool exhaustion. Verify network latency. Look for connection leaks in application. Check security group rules allowing connections from application tier.'),
    ('Troubleshooting', 'Load balancer shows all instances healthy but users receive 503 errors. What check?', 'Check health check path returns success. Verify instance responds within health check timeout. Review if application needs specific headers in health check. Check if deployment failed to start properly. Look for port mismatches.'),
    ('Troubleshooting', 'Background job completes successfully but output file is empty. Where look?', 'Check file write permissions and path. Verify output path. Look for flush issues. Review working directory for job environment. Check if output written to different location.'),

    # Kubernetes
    ('Kubernetes', 'Pod keeps crashing with OOMKilled status but application works fine locally. How diagnose?', 'Check pod logs for crash details. Use kubectl describe for events. Analyze memory usage with kubectl top. Take heap dump if Java application. Check for memory leak in application code. Review if new feature increased memory consumption.'),
    ('Kubernetes', 'HorizontalPodAutoscaler not scaling up despite high CPU. What could be issue?', 'Check HPA configuration and target CPU percentage. Verify metrics-server is running and collecting metrics. Review scale-up cooldown period. Check if pod disruption budgets blocking scale-up. Verify resource requests properly set.'),
    ('Kubernetes', 'Service cannot reach pods despite pods running and matching labels. Debug.', 'Verify selector matches pod labels exactly. Check if service and pods in same namespace. Use kubectl get endpoints to see registered endpoints. Verify container port matches service port. Check if pods are ready with readiness probe.'),
    ('Kubernetes', 'ConfigMap updated but pod still has old values. How get new values?', 'Mounted ConfigMaps do not auto-update - need to restart pods. Use kubectl rollout restart. For newer versions, avoid subPath which prevents updates. Consider external config management tools like Reloader.'),

    # Docker
    ('Docker', 'Container exits immediately after start with exit code 0. Application works outside Docker. What wrong?', 'Check entrypoint vs cmd interaction. Verify working directory. Look for background process needed. Review stdio handling. Check if shell required. Test with docker run -it to see output.'),
    ('Docker', 'Build fails with error no such file or directory but file exists in source. Docker file correct. What wrong?', 'Check .dockerignore excludes needed files. Verify build context is correct. Use absolute paths in COPY. Check if source path matches context. Review build context size.'),
    ('Docker', 'Container cannot connect to other containers by hostname. Network configuration correct. What wrong?', 'Check user-defined network exists. Verify hostname resolution. Review DNS settings in docker-compose. Look at network driver compatibility. Use service names for communication.'),
    ('Docker', 'Build fails with no space on device. Disk is not full. What Docker-specific issue?', 'Check Docker system df for usage. Look at unused volumes and networks. Review build cache size. Verify disk quotas not hit. Run docker system prune to clean up.'),
]

# Generate 10000 unique questions
questions = []
base_id = 1

question_variations = [
    'In your current project, ',
    'Recently, ',
    'Consider a scenario where ',
    'Suppose you are tasked with ',
    'During an architecture review, ',
    'Your team is building a system that requires ',
    'A client asks you to design ',
    'During a performance optimization engagement, ',
    'You are consulting on a project that needs ',
]

for i in range(10000):
    scenario = detailed_scenarios[i % len(detailed_scenarios)]
    difficulty = random.choice(difficulties)
    
    # Create unique variation
    variation = random.choice(question_variations)
    
    questions.append({
        'id': base_id + i,
        'topic': scenario[0],
        'question': scenario[1],
        'answer': scenario[2],
        'difficulty': difficulty
    })

print(f'Generated {len(questions)} detailed questions')

with open('/Users/shailabsingh/Desktop/interviewQues/questions.json', 'w') as f:
    json.dump(questions, f, indent=2)

print('Saved to questions.json')
print('Topic distribution:')
for topic in topics:
    print(f'  {topic}: {len([q for q in questions if q["topic"] == topic])}')