#!/usr/bin/env python3
import json
import random

def generate_questions():
    questions = []
    base_id = 1001
    
    mongodb_scenarios = [
        {"q": "Users report the search feature times out when searching product names with special characters. Some searches work, others don't. How would you diagnose and fix?", "a": "Check text index configuration for special character handling. Use case-insensitive regex with proper escaping. Consider using text index with language settings. Add input sanitization.", "d": "Medium"},
        {"q": "Your analytics team runs a monthly report that queries 50 million documents. It worked fine last month but now takes 3 hours. What changed and how to fix?", "a": "Check for missing indexes due to schema changes. Add covering indexes for common queries. Consider pre-aggregation with materialized views. Implement pagination. Use hint() to force index.", "d": "Hard"},
        {"q": "After a schema update, some embedded documents have null values where there should be objects. Users are seeing broken data. What went wrong?", "a": "Check update operations that modified the field. Verify default value handling. Look for $unset operations. Review migration script logic. Implement validation before updates.", "d": "Hard"},
        {"q": "Your real-time dashboard shows stale data. New writes don't appear immediately. Users see data that's 5 minutes old. How to get real-time updates?", "a": "Check read concern level. Use primary preferred read preference. Implement change streams for real-time. Add refresh on client. Check for caching layer issues.", "d": "Medium"},
        {"q": "The billing team can't generate invoices because the aggregation pipeline runs out of memory. The query worked before with same data size. What's happening?", "a": "Check allowDiskUse option in aggregation. Review $sort and $group stages causing memory. Add indexes to support pipeline stages. Break into smaller pipelines.", "d": "Hard"},
        {"q": "Your mobile app syncs offline data when connection restores. Some users report duplicate records after sync. How would you prevent duplicates?", "a": "Implement unique constraints on sync identifiers. Use upsert with proper key. Add conflict resolution with timestamps. Implement idempotent sync operations.", "d": "Medium"},
        {"q": "User sessions stored in MongoDB expire but aren't deleted. The collection grew to 100GB. How to clean up and prevent future buildup?", "a": "Create TTL index on expiration field. Set expireAfterSeconds appropriately. Use background job for cleanup verification. Check if fields are being set correctly.", "d": "Easy"},
        {"q": "Your recommendation engine queries user preferences but it's slow during peak hours. The dataset is only 1 million documents. What optimization would help?", "a": "Create compound index matching query patterns. Use projection to limit fields. Implement read/write splitting. Add Redis caching for hot data. Review query selectors.", "d": "Medium"},
        {"q": "During migration, some data got corrupted - fields that should be arrays contain strings. How to detect and fix this at scale?", "a": "Write validation script checking data types. Use $type operator to find mismatches. Create temporary field with correct type. Update using aggregation pipeline. Add schema validation.", "d": "Hard"},
        {"q": "Your GeoJSON location queries return wrong results. Points that should be within 5km aren't appearing. The coordinates are correct. What's wrong?", "a": "Check coordinate order - should be [longitude, latitude]. Verify 2dsphere index exists. Check coordinate format matches index type. Test with simpler query first.", "d": "Medium"},
    ]
    
    spring_scenarios = [
        {"q": "Users get 504 Gateway Timeout on file export. The export worked yesterday with same data. Now it fails after 30 seconds. What changed?", "a": "Check proxy timeout settings. Verify if data volume increased. Look for memory issues causing slow processing. Enable async processing. Check network latency.", "d": "Medium"},
        {"q": "Your API returns 401 for valid tokens. Users logged in yesterday can't access today. Tokens haven't expired. What's causing this?", "a": "Check token validation logic. Verify secret key hasn't changed. Look for JWT issuer changes. Check token blacklist implementation. Review clock skew handling.", "d": "Hard"},
        {"q": "Scheduled jobs run twice on some days. The cron is correct but duplicate executions happen. How to prevent this race condition?", "a": "Implement distributed locking with Redis. Add idempotency checks in job. Use @SchedulerLock annotation. Check for multiple scheduler instances.", "d": "Hard"},
        {"q": "Memory usage grows continuously until the app crashes. The team added a new feature last week. How to find the memory leak?", "a": "Take heap dumps and analyze with MAT. Profile with VisualVM. Check for unclosed resources. Review new feature for collections without cleanup.", "d": "Hard"},
        {"q": "API responses are slow during peak hours. The database looks fine. CPU usage on the app server is high. What's the bottleneck?", "a": "Check thread pool exhaustion. Increase connection pool size. Profile CPU hotspots. Use async controllers. Implement caching.", "d": "Medium"},
        {"q": "Users see other users' data when viewing their profiles. This is a critical security issue. How would you fix data isolation?", "a": "Check thread-local storage usage. Verify request-scoped beans. Review static field usage. Add proper session management. Implement tenant isolation.", "d": "Hard"},
        {"q": "The application won't start after adding a new dependency. Error shows 'BeanCreationException'. How to diagnose the startup failure?", "a": "Check dependency conflicts with mvn dependency:tree. Look for missing configuration. Review auto-configuration exclusions. Check component scanning.", "d": "Medium"},
        {"q": "WebSocket connections drop after a few minutes of inactivity. Reconnections work but users lose context. How to maintain persistent connections?", "a": "Configure WebSocket ping/pong intervals. Check proxy timeout settings. Implement heartbeat mechanism. Use STOMP for better control.", "d": "Medium"},
        {"q": "File upload fails with 'The temp file could not be renamed'. The server has plenty of disk space. What's causing this error?", "a": "Check temp directory permissions. Verify file system is not mounted read-only. Look for disk quota issues. Check file descriptor limits.", "d": "Easy"},
        {"q": "Metrics show high latency for one specific endpoint. Other endpoints are fast. The code hasn't changed. What could cause this?", "a": "Check for database query issues. Look for external service calls. Review caching behavior. Profile that specific endpoint. Check for connection pool issues.", "d": "Medium"},
    ]
    
    aws_scenarios = [
        {"q": "Your Lambda fails with 'Runtime exited unexpectedly' errors. The function worked before. No code changes were made. What would you check?", "a": "Check CloudWatch logs for errors. Verify function timeout settings. Look for memory limit issues. Check for dependency version changes. Review deployment package size.", "d": "Medium"},
        {"q": "S3 bucket shows thousands of requests per day but you don't know who's accessing it. How to investigate and secure?", "a": "Enable S3 access logging. Analyze logs for patterns. Check bucket policy. Review IAM users and roles. Implement bucket alerts.", "d": "Medium"},
        {"q": "EC2 instances keep being terminated by ASG unexpectedly. No errors in system logs. What would cause this?", "a": "Check health check configuration. Review CloudWatch metrics for liveness. Look for ELB deregistration delay. Verify instance health status.", "d": "Hard"},
        {"q": "Your RDS failed over to replica but the application couldn't connect after. The failover completed. What's blocking the connection?", "a": "Check connection string uses read endpoint. Verify security groups allow new primary. Review DNS caching. Update connection handling to handle failover.", "d": "Hard"},
        {"q": "CloudWatch billing alerts fire but you can't identify what service is costing money. How to breakdown costs by service?", "a": "Use Cost Explorer with service filtering. Enable detailed billing. Review Cost and Usage Report. Check Trusted Advisor recommendations.", "d": "Easy"},
        {"q": "Your NAT Gateway shows high byte count but you didn't launch any new services. Traffic spiked overnight. How to investigate?", "a": "Check flow logs for traffic patterns. Look forInstances in private subnets with outbound access. Identify unusual destinations. Review security groups.", "d": "Medium"},
        {"q": "ALB returns 403 on specific paths but works on others. Same origin works directly. What would cause this selective blocking?", "a": "Check WAF rules for path conditions. Review security groups for rules. Look at path-based routing. Verify header requirements.", "d": "Medium"},
        {"q": "Your CodePipeline fails at approval step with 'Pipeline not found' error. The pipeline existed yesterday. What happened?", "a": "Check if pipeline was accidentally deleted. Review CloudTrail for deletion events. Check for cross-region issues. Verify IAM permissions.", "d": "Hard"},
        {"q": "ECS tasks keep restarting with exit code 137. Memory usage looks normal in CloudWatch. What's causing the OOM kills?", "a": "Check container memory limits vs actual usage. Look for JVM heap settings. Review application memory management. Check for memory leaks.", "d": "Hard"},
        {"q": "Route 53 returns correct IP but users get wrong website. The DNS record is correct. What could be wrong?", "a": "Check for multiple record sets. Review health check configurations. Look for resolver cache issues. Verify hosted zone propagation.", "d": "Medium"},
    ]
    
    dsa_scenarios = [
        {"q": "Your sorting algorithm times out on 1 million records. The data is mostly sorted already but your algorithm doesn't leverage this. What's a better approach?", "a": "Use adaptive sorting algorithm like Timsort that detects pre-sorted runs. Consider insertion sort for nearly sorted data. Use hybrid approach based on run detection.", "d": "Hard"},
        {"q": "Your cache lookup is slow with millions of keys. Simple HashMap works but needs improvement. What data structure speeds this up?", "a": "Use concurrent hash map for thread safety. Implement sharding to reduce contention. Consider B-trees for range queries. Use perfect hashing for known keys.", "d": "Medium"},
        {"q": "Finding closest warehouse to customer takes too long. With 10,000 warehouses and millions of customers, this is slow. What's the efficient approach?", "a": "Use spatial indexing with R-tree or Quadtree. Implement geohash for quick filtering. Use KD-tree for nearest neighbor search. Pre-compute region mappings.", "d": "Hard"},
        {"q": "Your graph traversal for friend recommendations times out. The social graph has millions of nodes and edges. How to optimize traversal?", "a": "Use BFS with depth limits. Implement bidirectional search. Cache intermediate results. Use adjacency list with efficient storage. Consider pre-computation.", "d": "Hard"},
        {"q": "String matching for pattern search is slow. You need to find occurrences in gigabytes of text. What's faster than naive approach?", "a": "Use KMP algorithm for linear time matching. Implement Aho-Corasick for multiple patterns. Use suffix arrays for complex patterns. Consider indexed search.", "d": "Hard"},
        {"q": "Your recursion causes stack overflow on deep trees. Trees can have 100,000 nodes deep. How to handle such deep structures?", "a": "Convert recursive to iterative with explicit stack. Use tail recursion where possible. Implement node visiting without full path. Consider tree flattening.", "d": "Hard"},
        {"q": "Finding duplicate items in list takes too long. With 10 million items, O(n²) approach is too slow. What's the efficient solution?", "a": "Use HashSet for O(n) detection. Sort first then scan for O(n log n). Use Bloom filter for quick check. Implement external sorting for memory limits.", "d": "Medium"},
        {"q": "Your priority queue is slow for real-time ranking. Scores change frequently and you need top 100 from 1 million. What's efficient?", "a": "Use binary heap with lazy deletion. Implement tournament tree. Use Redis sorted set. Maintain sliding window of top items. Batch updates.", "d": "Hard"},
        {"q": "Searching for products by multiple filters is slow. Users apply 5+ filters on 1 million products. How to speed this up?", "a": "Create composite indexes matching filter combinations. Use bitmap indexes for categorical filters. Implement inverted index. Consider search engine.", "d": "Hard"},
        {"q": "Your maze solver runs out of memory on large mazes. The algorithm is correct but uses too much memory for big grids. What's memory-efficient?", "a": "Use A* with admissible heuristic. Implement BFS with frontier only. Use bidirectional search. Consider pathfinding with compression.", "d": "Hard"},
    ]
    
    troubleshooting_scenarios = [
        {"q": "Users see '502 Bad Gateway' errors intermittently. The backend services appear healthy. What would cause this inconsistent behavior?", "a": "Check ALB connection draining settings. Look for backend timeout mismatches. Review slow request handling. Check for periodic health check failures.", "d": "Medium"},
        {"q": "Database queries are slow but EXPLAIN shows index is being used. The query worked fast yesterday. What could have changed?", "a": "Check for statistics staleness. Look for data distribution changes. Verify index is not fragmented. Review table size growth.", "d": "Hard"},
        {"q": "Your API returns error 429 immediately on first request. You haven't hit any limit. The error message is vague. What's happening?", "a": "Check for client-side rate limiting. Review API key usage. Look at proxy configuration. Verify request headers aren't triggering limits.", "d": "Medium"},
        {"q": "Users report images fail to load on mobile only. Desktop works fine. Same image URLs work on desktop. What could cause this?", "a": "Check image size limits on mobile. Look at CDN configuration differences. Review mobile-specific SSL issues. Check for bandwidth throttling.", "d": "Medium"},
        {"q": "The application runs fine locally but fails in production. Same code, same database. What environment differences could cause this?", "a": "Check environment variables. Review configuration differences. Look for case sensitivity issues. Verify file path separators. Check timezone settings.", "d": "Medium"},
        {"q": "Background job runs successfully but doesn't produce expected output. Logs show it completed. Where did the output go?", "a": "Check output destination permissions. Look at file path resolution. Review working directory. Verify async processing completed.", "d": "Easy"},
        {"q": "Users report form submissions don't work on Safari. Same form works on Chrome and Firefox. What browser-specific issue?", "a": "Check CORS headers for Safari. Look at form encoding. Review JavaScript compatibility. Test with different Safari versions.", "d": "Medium"},
        {"q": "Your websocket connection keeps reconnecting every minute. The server appears fine. What would cause this ping-pong failure?", "a": "Check keepalive interval settings. Look at proxy timeout configuration. Review network latency. Verify server supports ping/pong.", "d": "Medium"},
        {"q": "API returns stale data even after database update. The update completes successfully. Cache should have expired. What's wrong?", "a": "Check cache TTL settings. Look for cache key issues. Verify cache invalidation on update. Review distributed cache consistency.", "d": "Hard"},
        {"q": "Your cron job runs at wrong time. The cron expression is correct but execution is 3 hours off. What's causing this?", "a": "Check server timezone vs cron timezone. Look at daylight saving handling. Verify cron daemon timezone. Review system timezone settings.", "d": "Easy"},
    ]
    
    kubernetes_scenarios = [
        {"q": "Pod fails with 'ImagePullBackOff' error. The image exists in registry and worked before. What would cause this?", "a": "Check image tag exists. Verify registry credentials. Look for namespace issues. Review image pull policy. Check for region problems.", "d": "Medium"},
        {"q": "Service can't reach pods - no endpoints available. Pods are running and healthy. What configuration is missing?", "a": "Verify selector matches pod labels. Check service port matches container port. Review endpoint creation. Check network policy.", "d": "Medium"},
        {"q": "Horizontal Pod Autoscaler isn't scaling up. Metrics show CPU at 80% but replicas stay at minimum. What's wrong?", "a": "Check HPA configuration. Verify metrics-server is running. Review scale-up cooldown period. Check resource requests vs limits.", "d": "Medium"},
        {"q": "Pod keeps getting evicted due to memory pressure. Other pods are fine. What's different about this pod?", "a": "Check memory requests vs limits. Look at pod priority. Review resource usage over time. Check for memory leaks. Verify QoS class.", "d": "Hard"},
        {"q": "ConfigMap changes aren't reflected in pod. You updated the ConfigMap but pod still has old values. How to trigger refresh?", "a": "Pods don't auto-update - need restart. Use volume mount with subPath prevents updates. Delete pods to force recreation. Use external config management.", "d": "Medium"},
        {"q": "Ingress returns 404 for valid paths. The service behind ingress works directly. What routing is misconfigured?", "a": "Check ingress path matching rules. Verify host header requirements. Review ingress controller logs. Check path type (Prefix vs Exact).", "d": "Medium"},
        {"q": "Secret values appear base64 encoded in logs when they shouldn't be. Is this a security concern?", "a": "Base64 encoding is for transmission, not encryption. Secrets are base64 in etcd. Enable encryption at rest. Use external secrets operator.", "d": "Medium"},
        {"q": "Pod can't resolve external DNS. Internal service discovery works. What network policy blocks external queries?", "a": "Check DNS policy (ClusterFirst vs Default). Verify CoreDNS is running. Look at network policies blocking egress. Check NAT gateway.", "d": "Medium"},
        {"q": "StatefulSet pods have hostname conflicts. Pods get same hostname and crash. What ordering issue exists?", "a": "Check ordinal indexing in StatefulSet. Verify PVC naming consistency. Review pod identity settings. Look at startup ordering.", "d": "Hard"},
        {"q": "Job keeps retrying but never succeeds. The job container exits with code 1. How to debug infinite retries?", "a": "Check job restart policy. Review backoff limit settings. Look at pod logs. Verify init container failures. Check resource limits.", "d": "Medium"},
    ]
    
    docker_scenarios = [
        {"q": "Container exits immediately after starting with code 0. No errors in logs. The app works outside Docker. What's wrong?", "a": "Check entrypoint vs cmd interaction. Verify working directory. Look for background process needed. Review stdio handling. Check shell required.", "d": "Medium"},
        {"q": "Docker build is slow - each layer takes minutes. The Dockerfile didn't change. What would cause this slowdown?", "a": "Check build context size. Review layer caching. Look for network issues. Verify registry response time. Check disk I/O.", "d": "Medium"},
        {"q": "Container uses excessive CPU but application code looks fine. Single process should not be this heavy. What's consuming resources?", "a": "Check for container startup overhead. Look at logging level. Review debug mode. Verify unnecessary processes. Check for infinite loops.", "d": "Medium"},
        {"q": "Volume mount shows empty in container. The host directory has files. Mount configuration looks correct. What could be wrong?", "a": "Check path on host vs container. Verify SELinux/AppArmor issues. Look at mount propagation. Review volume driver. Check directory creation.", "d": "Medium"},
        {"q": "Container can't connect to other containers by hostname. Links worked before. What network configuration changed?", "a": "Check user-defined network exists. Verify hostname resolution. Review DNS settings in docker-compose. Look at network driver.", "d": "Medium"},
        {"q": "Image build fails with 'no space left on device'. The disk is not full. What would cause this Docker-specific error?", "a": "Check Docker system df for usage. Look at unused volumes/networks. Review build cache size. Verify disk quotas. Clean up with docker system prune.", "d": "Easy"},
        {"q": "Container gets OOMKilled but memory limit is high. The app should use less than the limit. What's causing this?", "a": "Check for memory overhead beyond app. Look at JVM heap vs container limit. Review memory accounting. Verify cgroup memory accounting.", "d": "Hard"},
        {"q": "Multi-stage build produces huge final image. The dependencies should be small. What's included that shouldn't be?", "a": "Check COPY instructions in final stage. Review --from ordering. Look for unnecessary files. Verify .dockerignore. Check build artifacts.", "d": "Medium"},
        {"q": "Container can't resolve HTTPS sites. HTTP works fine. Same code works outside container. What TLS issue exists?", "a": "Check certificate authority certificates. Look at TLS version compatibility. Verify SNI support. Review DNS resolution for HTTPS.", "d": "Medium"},
        {"q": "Port mapping works locally but not from other machines. The service binds to localhost. How to fix for external access?", "a": "Bind to 0.0.0.0 instead of localhost. Check firewall rules. Verify port is not already in use. Review --network host mode.", "d": "Easy"},
    ]
    
    difficulties = ["Easy", "Medium", "Hard"]
    
    # Generate MongoDB questions (1000)
    for i in range(100):
        for scenario in mongodb_scenarios:
            difficulty = random.choice(difficulties)
            questions.append({
                "id": base_id + len(questions),
                "topic": "MongoDB",
                "question": scenario["q"],
                "answer": scenario["a"],
                "difficulty": difficulty
            })
            if len([q for q in questions if q["topic"] == "MongoDB"]) >= 1000:
                break
        if len([q for q in questions if q["topic"] == "MongoDB"]) >= 1000:
            break
    
    # Generate Spring Boot questions (1000)
    for i in range(100):
        for scenario in spring_scenarios:
            difficulty = random.choice(difficulties)
            questions.append({
                "id": base_id + len(questions),
                "topic": "Spring Boot",
                "question": scenario["q"],
                "answer": scenario["a"],
                "difficulty": difficulty
            })
            if len([q for q in questions if q["topic"] == "Spring Boot"]) >= 1000:
                break
        if len([q for q in questions if q["topic"] == "Spring Boot"]) >= 1000:
            break
    
    # Generate AWS questions (1000)
    for i in range(100):
        for scenario in aws_scenarios:
            difficulty = random.choice(difficulties)
            questions.append({
                "id": base_id + len(questions),
                "topic": "AWS",
                "question": scenario["q"],
                "answer": scenario["a"],
                "difficulty": difficulty
            })
            if len([q for q in questions if q["topic"] == "AWS"]) >= 1000:
                break
        if len([q for q in questions if q["topic"] == "AWS"]) >= 1000:
            break
    
    # Generate DSA questions (1000)
    for i in range(100):
        for scenario in dsa_scenarios:
            difficulty = random.choice(difficulties)
            questions.append({
                "id": base_id + len(questions),
                "topic": "DSA",
                "question": scenario["q"],
                "answer": scenario["a"],
                "difficulty": difficulty
            })
            if len([q for q in questions if q["topic"] == "DSA"]) >= 1000:
                break
        if len([q for q in questions if q["topic"] == "DSA"]) >= 1000:
            break
    
    # Generate Troubleshooting questions (1000)
    for i in range(100):
        for scenario in troubleshooting_scenarios:
            difficulty = random.choice(difficulties)
            questions.append({
                "id": base_id + len(questions),
                "topic": "Troubleshooting",
                "question": scenario["q"],
                "answer": scenario["a"],
                "difficulty": difficulty
            })
            if len([q for q in questions if q["topic"] == "Troubleshooting"]) >= 1000:
                break
        if len([q for q in questions if q["topic"] == "Troubleshooting"]) >= 1000:
            break
    
    # Generate Kubernetes questions (500)
    for i in range(50):
        for scenario in kubernetes_scenarios:
            difficulty = random.choice(difficulties)
            questions.append({
                "id": base_id + len(questions),
                "topic": "Kubernetes",
                "question": scenario["q"],
                "answer": scenario["a"],
                "difficulty": difficulty
            })
            if len([q for q in questions if q["topic"] == "Kubernetes"]) >= 500:
                break
        if len([q for q in questions if q["topic"] == "Kubernetes"]) >= 500:
            break
    
    # Generate Docker questions (500)
    for i in range(50):
        for scenario in docker_scenarios:
            difficulty = random.choice(difficulties)
            questions.append({
                "id": base_id + len(questions),
                "topic": "Docker",
                "question": scenario["q"],
                "answer": scenario["a"],
                "difficulty": difficulty
            })
            if len([q for q in questions if q["topic"] == "Docker"]) >= 500:
                break
        if len([q for q in questions if q["topic"] == "Docker"]) >= 500:
            break
    
    # Now read existing questions and merge
    try:
        with open('/Users/shailabsingh/Desktop/interviewQues/questions.json', 'r') as f:
            existing = json.load(f)
        # Reassign IDs to avoid conflicts
        for i, q in enumerate(existing):
            q['id'] = i + 1
        questions = existing + questions
    except:
        pass
    
    # Trim to exactly 6000 if over
    questions = questions[:6000]
    
    # Reassign all IDs sequentially
    for i, q in enumerate(questions):
        q['id'] = i + 1
    
    with open('/Users/shailabsingh/Desktop/interviewQues/questions.json', 'w') as f:
        json.dump(questions, f, indent=2)
    
    print(f"Total questions: {len(questions)}")
    counts = {}
    for q in questions:
        counts[q['topic']] = counts.get(q['topic'], 0) + 1
    for topic, count in counts.items():
        print(f"{topic}: {count}")

if __name__ == '__main__':
    generate_questions()