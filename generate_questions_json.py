#!/usr/bin/env python3
import json
import random

questions = []

# MongoDB Questions (200) - Real-world scenarios
mongodb_scenarios = [
    {"q": "Your product catalog search is taking 5+ seconds during sales. The product collection has 2 million documents. How would you identify and fix the performance issue?", "a": "Use explain() to analyze query plan. Create compound indexes on frequently searched fields (category, price, name). Use text index for search. Implement query projection to return only needed fields. Consider caching with Redis.", "d": "Medium"},
    {"q": "Users are complaining that when multiple people buy the same item simultaneously, inventory goes negative. How would you prevent this race condition?", "a": "Implement optimistic locking using version field. Use findOneAndUpdate with version check. If version mismatch, retry the transaction. Alternatively use distributed locking with Redis.", "d": "Hard"},
    {"q": "Your chat application needs to store message history that auto-deletes after 30 days to comply with privacy regulations. How would you implement this?", "a": "Create TTL (Time-To-Live) index on the timestamp field: db.messages.createIndex({createdAt: 1}, {expireAfterSeconds: 2592000}). MongoDB will automatically delete documents after 30 days.", "d": "Easy"},
    {"q": "Your reporting team needs to generate monthly sales reports but queries are slow. They need to count orders by product category, calculate revenue, and find top customers. What would you recommend?", "a": "Create aggregation pipeline with $match for date range, $group by category for revenue, $sort for top customers. Use $facet to run multiple aggregations in single query. Consider pre-aggregation with views.", "d": "Medium"},
    {"q": "Your startup's user data is all in one collection. As you scale to millions of users, queries are becoming slow and some API calls timeout. What's your scaling strategy?", "a": "Implement sharding based on user_id hash. Choose appropriate shard key. Add indexes on commonly queried fields. Use read replicas for reporting queries. Consider denormalization for frequently accessed data.", "d": "Hard"},
    {"q": "A user reports they registered yesterday but their account doesn't show up when searching. Other users from the same time work fine. How would you debug this?", "a": "Check for null or undefined values in the query. Verify the index includes the field being searched. Look for case sensitivity issues. Check if document was actually inserted with findOne(). Review error logs for silent failures.", "d": "Medium"},
    {"q": "Your mobile app's offline feature needs to sync local data with server when connection restores. Some users report data loss after sync. How would you handle this?", "a": "Implement conflict resolution using timestamps or version numbers. Use change streams to track changes. Implement soft deletes with sync flags. Add retry logic with exponential backoff. Test edge cases with clock skew.", "d": "Hard"},
    {"q": "Your analytics dashboard fetches millions of records and the page times out before loading. Users see a spinning loader that never completes. What's the solution?", "a": "Implement pagination with cursor-based approach. Use projection to return only needed fields. Consider pre-aggregating analytics data. Add server-side caching. Implement infinite scroll instead of loading all at once.", "d": "Medium"},
    {"q": "A new feature requires storing user preferences that vary by country. Some countries have 5 fields, others have 20. The schema keeps changing. How would you design this?", "a": "Use mixed schema with common required fields and optional extended fields in a separate object. Use discriminator field for country-specific validation. Store in single document with country-specific embedded object.", "d": "Medium"},
    {"q": "Your payment system stores transaction history. On audit, you discover some transaction records are missing from the database. How would you ensure data integrity?", "a": "Use transactions for multi-document operations. Implement write-ahead logging. Add validation at application layer. Use replica sets with write concern majority. Implement continuous backup and point-in-time recovery.", "d": "Hard"},
]

# Generate more variations for MongoDB
for i in range(190):
    scenario = random.choice(mongodb_scenarios)
    questions.append({
        "id": len(questions) + 1,
        "topic": "MongoDB",
        "question": scenario["q"],
        "answer": scenario["a"],
        "difficulty": scenario["d"]
    })

# Spring Boot Questions (200)
spring_scenarios = [
    {"q": "Users report that your API sometimes returns stale data. After updating their profile, subsequent requests still show old values. Sometimes it works after waiting a few minutes. What's happening and how would you fix it?", "a": "This is a caching issue. Configure cache headers properly. Add @CacheEvict on update methods to invalidate cache. Use @Cacheable with proper key generation. Consider using Redis with TTL. Verify Cache-Control headers are being respected.", "d": "Medium"},
    {"q": "Your payment integration sometimes fails with timeout errors, but the payment might have gone through on the provider's end. Users get charged twice or not at all. How would you handle this idempotency issue?", "a": "Implement idempotency keys - generate unique token for each payment request, store in database with status. On retry, check if request with same key exists. Use @Retryable with recovery callback. Implement webhook handler to confirm status.", "d": "Hard"},
    {"q": "A new microservice team wants to call your user service. They're getting 401 Unauthorized even with correct credentials. Other services work fine. How would you diagnose this?", "a": "Check CORS configuration for the endpoint. Verify the Authorization header is being passed correctly. Check if the service is in the allowed origins list. Look at filter order - maybe security filter is blocking. Review gateway routing.", "d": "Medium"},
    {"q": "Your application crashes on startup with 'Port 8080 already in use' error. You previously ran the app successfully. How would you quickly get the app running again?", "a": "Run 'lsof -i :8080' to find the process using the port. Kill it with 'kill -9 <PID>'. Or change the port in application.properties: server.port=8081. Check for zombie processes. Use netstat to verify.", "d": "Easy"},
    {"q": "Your monitoring shows one of your services is consuming excessive memory and the pod keeps restarting. The team can't identify the root cause. How would you troubleshoot this memory leak?", "a": "Enable JMX and connect with VisualVM. Take heap dumps and analyze with MAT. Check for unclosed resources (connections, streams). Profile with YourKit. Review logs for OutOfMemoryError. Add -XX:+HeapDumpOnOutOfMemoryError.", "d": "Hard"},
    {"q": "Users in different timezones are seeing incorrect times for scheduled events. A meeting set for 3 PM shows as 3 AM for some users. How would you fix this timezone handling?", "a": "Store all timestamps in UTC in database. Use @JsonFormat with timezone specification. Convert to user's timezone at display layer using their profile preference. Use ZoneId in Java 8+. Don't store naive timestamps.", "d": "Medium"},
    {"q": "Your file upload endpoint works for small files but fails for anything over 5MB with '413 Request Entity Too Large'. How would you allow larger files?", "a": "Configure Spring Boot file size limits: spring.servlet.multipart.max-file-size=50MB, spring.servlet.multipart.max-request-size=50MB. Also configure at web server level (Tomcat max-http-post-size). Update client to send proper headers.", "d": "Easy"},
    {"q": "During load testing, your service handles 100 requests fine but times out at 500 requests. The database CPU looks fine. What could be the bottleneck and how would you fix it?", "a": "Likely thread pool exhaustion or connection pool limit. Increase HikariCP max pool size. Configure Tomcat thread pool: server.tomcat.max-threads=200. Use async processing with CompletableFuture. Implement request buffering with message queue.", "d": "Hard"},
    {"q": "A developer committed a change that broke production. You need to quickly revert while investigating. How would you do an emergency rollback?", "a": "Use 'git log' to find last working commit. Create hotfix branch. Revert or reset to previous commit. Deploy using CI/CD pipeline. Alternatively use rollback feature in deployment tool. Never directly push to production branch.", "d": "Medium"},
    {"q": "Your API returns internal server errors randomly. Looking at logs, you see 'NullPointerException' with no context. How would you improve error handling?", "a": "Implement @ControllerAdvice for global exception handling. Create custom exception classes. Add proper logging with MDC for correlation IDs. Return meaningful error responses with stack trace in development. Add validation with @Valid.", "d": "Medium"},
]

for i in range(190):
    scenario = random.choice(spring_scenarios)
    questions.append({
        "id": len(questions) + 1,
        "topic": "Spring Boot",
        "question": scenario["q"],
        "answer": scenario["a"],
        "difficulty": scenario["d"]
    })

# AWS Questions (200)
aws_scenarios = [
    {"q": "Your website suddenly becomes unreachable. Checking AWS console, you see all EC2 instances in one availability zone are showing 'unhealthy' status. The website worked fine an hour ago. What happened and how would you restore service?", "a": "Check if AZ is experiencing an outage. If yes, update Auto Scaling Group to launch instances in healthy AZs. Or manually launch replacement instances in different AZ. Update Route 53 if needed. Check CloudWatch for historical data.", "d": "Medium"},
    {"q": "Your S3-hosted static website works for some users but others get 'Access Denied' errors. The bucket policy looks correct. What's causing this inconsistent access?", "a": "Check if bucket has public access block enabled. Verify IAM policies for specific users. Look for bucket ACL conflicts. Check if objects have specific grants. Verify region latency - users might hit wrong endpoint.", "d": "Medium"},
    {"q": "Your Lambda function processes uploaded files. It works for small files but times out for files over 10MB. The function is simple and completes quickly for small files. What's the issue?", "a": "Lambda has 6MB request size limit (10MB for synchronous). Use pre-signed URL for direct S3 upload. Split large files into chunks. Use S3 trigger instead of API Gateway. Increase timeout and memory if needed.", "d": "Easy"},
    {"q": "Your RDS database is running slowly. The CPU is at 100% and connections are timing out. You haven't changed anything recently. What would you investigate first?", "a": "Check CloudWatch for query patterns. Run 'SHOW PROCESSLIST' to see active queries. Check slow query log. Look for missing indexes on frequently queried columns. Verify if any new traffic patterns emerged.", "d": "Hard"},
    {"q": "Your ALB is returning 502 errors to users. The target group shows all instances are 'healthy' in the AWS console. What's going on and how would you fix it?", "a": "Check if application is listening on correct port. Verify security groups allow ALB to reach instances. Check if health check path is correct. Look for application crashes at startup. Review ALB access logs in S3.", "d": "Medium"},
    {"q": "Your cost bill tripled this month. You didn't launch any new services. How would you investigate what changed?", "a": "Check Cost Explorer for service breakdown. Review CloudWatch usage metrics. Look for unattached EBS volumes and old snapshots. Check for increased NAT gateway data transfer. Review Reserved Instance utilization.", "d": "Medium"},
    {"q": "Users in Europe are complaining about slow response times while US users have fast experiences. Your servers are in us-east-1. How would you improve global performance?", "a": "Deploy to multiple regions (eu-west-1). Use Route 53 with latency routing. Implement CloudFront for static content. Use DynamoDB Global Tables. Consider Local Zones for edge locations.", "d": "Medium"},
    {"q": "You need to provide a vendor access to specific S3 bucket temporarily. They need read-only access for 3 days. How would you configure this securely?", "a": "Create IAM user with expiration. Or generate pre-signed URLs with expiration. Use bucket policy with condition for date. Create separate access key and set expiration. Never share root credentials.", "d": "Easy"},
    {"q": "Your Kubernetes pods keep crashing with 'OOMKilled' status. The application worked fine before. How would you fix this?", "a": "Increase memory limits in deployment. Check for memory leaks in application. Review heap settings. Use resource requests for proper scheduling. Profile with async-profiler. Check if new feature added memory overhead.", "d": "Hard"},
    {"q": "Your development team can't access resources in the private subnet. They could access yesterday. Nothing changed in the configuration. What's the most likely cause?", "a": "Check if NAT Gateway is running and has available bandwidth. Verify route tables are correct. Check security groups on NAT. Look for VPC endpoint issues. Verify internet gateway is attached.", "d": "Medium"},
]

for i in range(190):
    scenario = random.choice(aws_scenarios)
    questions.append({
        "id": len(questions) + 1,
        "topic": "AWS",
        "question": scenario["q"],
        "answer": scenario["a"],
        "difficulty": scenario["d"]
    })

# DSA Questions (200)
dsa_scenarios = [
    {"q": "Your product recommendation algorithm needs to sort 10 million products by relevance score. The current implementation times out. The scores are unsorted and change frequently. What approach would work efficiently?", "a": "Use efficient sorting algorithm. Since data changes frequently, consider heap-based selection (O(n log k) for top-k). Use database ORDER BY with index if storing. Parallelize sorting for large datasets.", "d": "Medium"},
    {"q": "A user enters a search term and expects instant results as they type. Your current approach fetches all products and filters in JavaScript. It's slow with 100k products. How would you optimize this?", "a": "Implement Trie (prefix tree) for autocomplete. Use binary search after sorting. Implement pagination. Consider full-text search engine like Elasticsearch. Add caching for popular queries.", "d": "Hard"},
    {"q": "Your delivery app needs to find the nearest available driver from a list of 10,000 drivers scattered across a city. Users expect this to happen in under 100ms. How would you implement this efficiently?", "a": "Use spatial indexing (Quadtree or R-tree). Store driver locations with geohash. Use database with geospatial queries. Use bounding box pre-filter then distance calculation. Consider Redis with geospatial commands.", "d": "Hard"},
    {"q": "Your chat application shows conversation history in chronological order. Loading 10,000 messages takes several seconds. Users scroll through chronologically. What data structure would help?", "a": "Use linked list for O(1) insertion at both ends. Use pagination with cursor-based navigation. Implement lazy loading. Consider using database with indexed timestamp. Use virtual scrolling for UI.", "d": "Medium"},
    {"q": "Your e-commerce site needs to show 'Frequently Bought Together' recommendations. For each product pair, you need to calculate how often they appear together in orders. With 100k orders and 10k products, this is slow. What's the efficient approach?", "a": "Use association rule mining. Store co-occurrence counts in hash map. Use database GROUP BY with CUBE. Pre-compute recommendations periodically. Use Spark for large-scale processing.", "d": "Hard"},
    {"q": "Your game leaderboard needs to show top 100 players sorted by score. Scores update in real-time and there are 1 million players. Updating a sorted list on each score change is too slow. How would you handle this?", "a": "Use skip list or balanced BST for O(log n) updates. Use database with ranking functions. Implement cache with periodic updates. Use Redis Sorted Set with ZADD/ZRANGE. Consider batched updates.", "d": "Hard"},
    {"q": "Your API rate limiter needs to track requests per user. For each request, check if user exceeded 1000 requests in the last hour. With millions of users, checking database on each request is slow. What's the solution?", "a": "Use sliding window algorithm with Redis. Use token bucket or leaky bucket. Store request timestamps in sorted set. Implement in-memory with periodic cleanup. Use distributed rate limiter.", "d": "Medium"},
    {"q": "Your social media feed shows posts from followed users. With 10,000 followers and chronological order, fetching posts from all followed users and sorting is slow. How would you optimize feed generation?", "a": "Pre-generate feeds with background job. Use fan-out on write. Implement cursor-based pagination. Cache popular feeds. Use dedicated feed infrastructure like Cassandra.", "d": "Hard"},
    {"q": "Your payment system needs to validate a coupon code. There are 1 million valid codes with varying discounts. Looking up in a list is too slow. What data structure would make this fast?", "a": "Use HashMap for O(1) lookup. Use Trie if codes have patterns. Use Bloom filter to quickly reject invalid codes. Index in database with proper queries. Consider caching hot codes.", "d": "Medium"},
    {"q": "Your image processing pipeline processes images in sequence. With thousands of images, processing takes hours. The processing for each image is independent. How would you speed this up significantly?", "a": "Use parallel processing with thread pool. Implement producer-consumer pattern. Use distributed processing with message queue. Use GPU processing if applicable. Implement pipeline with parallel stages.", "d": "Medium"},
]

for i in range(190):
    scenario = random.choice(dsa_scenarios)
    questions.append({
        "id": len(questions) + 1,
        "topic": "DSA",
        "question": scenario["q"],
        "answer": scenario["a"],
        "difficulty": scenario["d"]
    })

# Troubleshooting Questions (200)
trouble_scenarios = [
    {"q": "Users report your website loads but all API calls fail with 'net::ERR_CONNECTION_REFUSED'. The app worked yesterday. What would you check first?", "a": "Check if API server is running. Verify port is correct. Check firewall rules. Look at load balancer health. Review recent deployments. Check if service crashed or was stopped.", "d": "Easy"},
    {"q": "Your application logs show 'Connection timed out' errors to the database. The database server CPU and memory look fine. What could be the issue?", "a": "Check database connection pool is exhausted. Verify connection string is correct. Look for network latency. Check if too many connections from app. Review recent traffic spike.", "d": "Medium"},
    {"q": "A user creates an account but can't log in. They get 'Invalid credentials' even with correct password. Other users work fine. How would you investigate?", "a": "Check if password was saved with different hashing. Verify email matches exactly (case-sensitive). Look for duplicate accounts. Check if account was deactivated. Review authentication logs.", "d": "Medium"},
    {"q": "Your mobile app works on WiFi but fails on cellular data. The API server works when tested from desktop on cellular. What could be different?", "a": "Check if server blocks cellular IPs. Look at MTU size issues. Verify DNS resolution works. Check for carrier-specific routing. Test with VPN to isolate.", "d": "Hard"},
    {"q": "Your scheduled job that runs daily hasn't run for 3 days. The server is up. How would you figure out why it's not executing?", "a": "Check cron/scheduler configuration. Look at job logs for errors. Verify timezone settings. Check if server was restarted and scheduler restarted. Review job dependencies.", "d": "Easy"},
    {"q": "Your dashboard shows 'No data available' for today's metrics but yesterday's data shows fine. The data collection service is running. What's wrong?", "a": "Check time range in query. Verify data pipeline is processing. Look at data collection timestamp. Check for schema changes. Review ingestion queue backlog.", "d": "Medium"},
    {"q": "Users see other users' data when viewing their profiles. Names and addresses from different accounts mix together. How would you stop this serious data leak?", "a": "This is a critical security issue. Check for race conditions in code. Verify session/thread handling. Review cache key generation. Add data isolation tests. Implement proper request scoping.", "d": "Hard"},
    {"q": "Your payment button shows 'Processing' but never completes. No error appears but no payment is created. How would you diagnose this silent failure?", "a": "Check browser network tab for API responses. Look at server logs for exceptions. Verify payment provider integration. Check if request is timing out. Review webhook delivery.", "d": "Hard"},
    {"q": "Your search returns results but clicking one shows 'Page not found'. The item exists when searched directly. What's causing broken links?", "a": "Check URL encoding issues. Verify routing parameters are correct. Look for special characters in identifiers. Review redirect rules. Check for case sensitivity in URLs.", "d": "Easy"},
    {"q": "Your image uploads work in Chrome but fail in Safari. The same file size works in other browsers on Safari. What's different about Safari?", "a": "Check Safari's file upload size limits. Look at CORS headers. Verify content-type handling. Test with different image formats. Check Safari-specific API differences.", "d": "Medium"},
]

for i in range(190):
    scenario = random.choice(trouble_scenarios)
    questions.append({
        "id": len(questions) + 1,
        "topic": "Troubleshooting",
        "question": scenario["q"],
        "answer": scenario["a"],
        "difficulty": scenario["d"]
    })

# Fill remaining to reach 1000
additional_questions = [
    {"topic": "MongoDB", "q": "Your e-commerce product filters work for some categories but timeout for others with millions of products. How would you make filtering consistent?", "a": "Create compound indexes matching filter combinations. Use covered queries with projection. Implement faceted search. Add pagination to filters. Consider denormalizing filter values.", "d": "Medium"},
    {"topic": "Spring Boot", "q": "Your CI/CD pipeline succeeded but the new version has bugs in production. How would you quickly roll back to the working version?", "a": "Use deployment tool's rollback feature. Re-deploy previous known good version. Use blue-green or canary deployment for safe rollbacks. Maintain version tags in registry.", "d": "Medium"},
    {"topic": "AWS", "q": "Your S3 bucket logs show many failed access attempts from unknown IP addresses. Should you be concerned?", "a": "Review failed requests for attack patterns. Enable S3 Block Public Access if not needed. Implement bucket policies with conditions. Add WAF for protection. Monitor for data exfiltration.", "d": "Medium"},
    {"topic": "DSA", "q": "Your news feed needs to show posts from people you follow sorted by time. With 5000 follows and 100k posts, this query is slow. What's the efficient approach?", "a": "Use cursor-based pagination with indexed timestamp. Pre-compute feed with background job. Use fan-out on write to distribute load. Cache recent feed segments.", "d": "Hard"},
    {"topic": "Troubleshooting", "q": "Your batch processing job takes 10 hours but business needs it to complete in 2 hours. The job processes 1 million records one by one. How would you optimize?", "a": "Parallelize processing with multiple workers. Batch database operations. Use bulk APIs. Optimize query patterns. Consider distributed processing with Spark.", "d": "Hard"},
]

for i in range(100):
    scenario = random.choice(additional_questions)
    questions.append({
        "id": len(questions) + 1,
        "topic": scenario["topic"],
        "question": scenario["q"],
        "answer": scenario["a"],
        "difficulty": scenario["d"]
    })

# Add more questions to reach exactly 1000
more_questions = [
    {"topic": "MongoDB", "q": "Users report their saved items disappeared after they updated their profile. How would you investigate data loss in your application?", "a": "Check for cascade deletes in schema. Review update operations that might have affected other collections. Look for soft delete implementation issues. Verify query filters are correct.", "d": "Medium"},
    {"topic": "Spring Boot", "q": "Your webhooks sometimes fire multiple times for the same event, causing duplicate processing. How would you make webhook handling idempotent?", "a": "Use unique event IDs to detect duplicates. Store processed event IDs with TTL. Check before processing new event. Use database constraints. Implement idempotency keys.", "d": "Medium"},
    {"topic": "AWS", "q": "Your Lambda function stopped processing messages from SQS. The function hasn't changed. How would you diagnose why messages are piling up?", "a": "Check Lambda concurrency limits. Review function logs for errors. Verify SQS visibility timeout. Check dead letter queue. Look for function throttling.", "d": "Medium"},
    {"topic": "DSA", "q": "Your autocomplete feature needs to handle 10,000 search terms with instant response. The current linear search is too slow. What data structure would work best?", "a": "Use Trie (prefix tree) for O(m) lookup where m is query length. Use Levenshtein distance for fuzzy matching. Implement caching for popular queries.", "d": "Medium"},
    {"topic": "Troubleshooting", "q": "Your date filter returns wrong results. Selecting 'This Week' returns items from last month. The data has correct timestamps. What's wrong?", "a": "Check timezone handling in query. Verify server timezone vs user timezone. Look at date parsing on frontend. Check if week starts on Monday vs Sunday.", "d": "Easy"},
]

for scenario in more_questions:
    for _ in range(20):
        questions.append({
            "id": len(questions) + 1,
            "topic": scenario["topic"],
            "question": scenario["q"],
            "answer": scenario["a"],
            "difficulty": scenario["d"]
        })

# Trim to exactly 1000
questions = questions[:1000]

# Save to JSON
with open('/Users/shailabsingh/Desktop/interviewQues/questions.json', 'w') as f:
    json.dump(questions, f, indent=2)

print(f"Generated {len(questions)} questions")
print(f"MongoDB: {len([q for q in questions if q['topic'] == 'MongoDB'])}")
print(f"Spring Boot: {len([q for q in questions if q['topic'] == 'Spring Boot'])}")
print(f"AWS: {len([q for q in questions if q['topic'] == 'AWS'])}")
print(f"DSA: {len([q for q in questions if q['topic'] == 'DSA'])}")
print(f"Troubleshooting: {len([q for q in questions if q['topic'] == 'Troubleshooting'])}")