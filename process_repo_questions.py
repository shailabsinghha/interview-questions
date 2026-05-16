#!/usr/bin/env python3
"""
Process interview questions from GitHub repos and merge into questions.json.
Extracts Q&A from:
1. 30-seconds-of-interviews (by fetching individual question files)
2. System design primer (hardcoded Q&A from solutions)
3. Backend interview questions (with generated answers)
4. ML interview questions
Deduplicates against existing questions.json.
"""
import json
import urllib.request
import urllib.error
import re
import sys
import os
import hashlib
import time

QUESTIONS_JSON = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'questions.json')

def fetch_url(url, max_retries=3):
    """Fetch a URL with retries."""
    for attempt in range(max_retries):
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=15) as resp:
                return resp.read().decode('utf-8')
        except Exception as e:
            if attempt < max_retries - 1:
                time.sleep(1)
                continue
            print(f"  Failed to fetch {url}: {e}")
            return None

def fetch_json(url):
    """Fetch a JSON URL."""
    content = fetch_url(url)
    if content:
        try:
            return json.loads(content)
        except json.JSONDecodeError as e:
            print(f"  JSON parse error: {e}")
    return None

def extract_qa_from_markdown(content, default_topic="JavaScript"):
    """Extract Q&A from a 30-seconds-of-interviews style markdown file."""
    questions = []
    
    # The files use format:
    # ### Question title
    #
    # #### Answer
    # ... answer text ...
    #
    # #### Good to hear
    # ... optional ...
    
    blocks = re.split(r'^### ', content, flags=re.MULTILINE)
    
    for block in blocks:
        if not block.strip():
            continue
        
        lines = block.split('\n')
        question_text = lines[0].strip()
        
        # Get everything after #### Answer header within this block
        answer_match = re.search(r'#### Answer\s*\n+(.*?)(?:\n#### |\Z)', block, re.DOTALL)
        if not answer_match:
            continue
        answer_text = answer_match.group(1).strip()
        
        # Remove additional meta sections from answer
        answer_text = re.split(r'#### Good to hear', answer_text)[0].strip()
        answer_text = re.split(r'##### Additional Links', answer_text)[0].strip()
        answer_text = re.split(r'##### Further Reading', answer_text)[0].strip()
        answer_text = re.split(r'##### Notes', answer_text)[0].strip()
        
        # Clean up excessive whitespace
        answer_text = re.sub(r'\n{3,}', '\n\n', answer_text)
        
        # Skip empty questions or answers
        if not question_text or not answer_text:
            continue
            
        # Determine difficulty based on complexity
        difficulty = "Medium"
        if len(answer_text) < 150:
            difficulty = "Easy"
        elif len(answer_text) > 500:
            difficulty = "Hard"
            
        questions.append({
            "question": question_text,
            "answer": answer_text[:2000],  # Truncate very long answers
            "topic": default_topic,
            "difficulty": difficulty
        })
    
    return questions

def fetch_30_seconds_questions():
    """Fetch all Q&A from 30-seconds-of-interviews by downloading individual files."""
    print("\n=== Fetching 30-seconds-of-interviews questions ===")
    questions = []
    
    # Get the questions directory listing
    api_url = "https://api.github.com/repos/Chalarangelo/30-seconds-of-interviews/contents/questions"
    files = fetch_json(api_url)
    
    if not files:
        print("  Failed to get file listing")
        return questions
    
    # Filter for markdown files (skip .eslintrc.js etc)
    md_files = [f for f in files if f['name'].endswith('.md')]
    print(f"  Found {len(md_files)} markdown question files")
    
    # Topic mapping based on filename prefixes
    topic_map = {
        'accessibility': 'Accessibility',
        'alt': 'HTML',
        'async': 'JavaScript',
        'batches': 'JavaScript',
        'bem': 'CSS',
        'big-o': 'DSA',
        'bind': 'JavaScript',
        'cache': 'HTML',
        'callback': 'JavaScript',
        'children': 'React',
        'class-name': 'React',
        'clone': 'JavaScript',
        'closure': 'JavaScript',
        'comparing': 'JavaScript',
        'context': 'React',
        'cors': 'JavaScript',
        'css-': 'CSS',
        'debouncing': 'JavaScript',
        'dom': 'JavaScript',
        'double-vs-triple': 'JavaScript',
        'element-vs-component': 'React',
        'em-rem': 'CSS',
        'error-boundaries': 'React',
        'event-delegation': 'JavaScript',
        'event-driven': 'JavaScript',
        'expression-vs-statement': 'JavaScript',
        'fibonacci': 'JavaScript',
        'float': 'JavaScript',
        'fragments': 'React',
        'frontend': 'HTML',
        'functional-programming': 'JavaScript',
        'higher-order': 'React',
        'hoisting': 'JavaScript',
        'html-': 'HTML',
        'i18n': 'HTML',
        'ii fe': 'JavaScript',
        'imperative-vs-declarative': 'JavaScript',
        'inline-conditional': 'React',
        'keyed-fragments': 'React',
        'keys': 'React',
        'lexical-vs-dynamic': 'JavaScript',
        'lifecycle': 'React',
        'lifting-state': 'React',
        'local-storage': 'HTML',
        'map-vs-foreach': 'JavaScript',
        'mask-string': 'JavaScript',
        'media-queries': 'CSS',
        'memoization': 'JavaScript',
        'mime': 'JavaScript',
        'mutable-vs-immutable': 'JavaScript',
        'nan': 'JavaScript',
        'node-': 'Node.js',
        'null-vs-undefined': 'JavaScript',
        'object-creation': 'JavaScript',
        'parameters-vs-arguments': 'JavaScript',
        'pass-by-reference': 'JavaScript',
        'passing-arguments': 'React',
        'pipe': 'JavaScript',
        'portals': 'React',
        'postfix-vs-prefix': 'JavaScript',
        'promise-states': 'JavaScript',
        'promises': 'JavaScript',
        'prop-validation': 'React',
        'prototypal-inheritance': 'JavaScript',
        'pure-function': 'JavaScript',
        'recursion': 'JavaScript',
        'refs': 'React',
        'rest': 'Node.js',
        'script-tag': 'HTML',
        'semicolons': 'JavaScript',
        'short-circuit': 'JavaScript',
        'sibling-selectors': 'CSS',
        'specificity': 'CSS',
        'sprites': 'CSS',
        'stateful-component': 'React',
        'stateless-component': 'React',
        'static-vs-instance': 'JavaScript',
        'sync-vs-async': 'JavaScript',
        'this-keyword': 'JavaScript',
        'truthy-falsy': 'JavaScript',
        'typeof': 'JavaScript',
        'ui-lib-frameworks': 'JavaScript',
        'use-strict': 'JavaScript',
        'var-let-const': 'JavaScript',
        'virtual-dom': 'JavaScript',
        'web-storage': 'HTML',
        'xss': 'Security',
    }
    
    for md_file in md_files:
        url = md_file['download_url']
        content = fetch_url(url)
        if not content:
            continue
        
        # Determine topic from filename
        fname = md_file['name'].lower()
        topic = "JavaScript"  # default
        for key, val in topic_map.items():
            if fname.startswith(key):
                topic = val
                break
        
        qas = extract_qa_from_markdown(content, topic)
        questions.extend(qas)
        print(f"  Got {len(qas)} Q&A from {md_file['name']}")
    
    print(f"  Total 30-seconds questions: {len(questions)}")
    return questions


def get_system_design_questions():
    """Return curated system design questions from system-design-primer."""
    print("\n=== Adding system design questions ===")
    questions = [
        {
            "topic": "System Design",
            "question": "Design Pastebin.com (or Bit.ly). Users enter a block of text and get a randomly generated link with optional expiration. Users can view paste contents via the link. The service needs to handle 10M users, 10M writes/month, 100M reads/month.",
            "answer": "Use a relational database as a hash table mapping shortlinks to paste locations. Generate unique URLs via MD5 hash of user IP + timestamp, Base62 encoded, take first 7 chars (62^7 possible values). Store paste content in object store (S3). Use REST API for create/get. Scale with: load balancer + web servers, CDN for static content, master-slave DB replication, memory cache (Redis) for hot pastes, and MapReduce for analytics. Considerations: cache-aside pattern, database sharding for write scaling, federation.",
            "difficulty": "Hard"
        },
        {
            "topic": "System Design",
            "question": "Design Twitter timeline and search (or Facebook feed). Users post tweets, view their timeline, view home timeline (from followed users), and search keywords. Handle 100M active users, 500M tweets/day, 250B read requests/month.",
            "answer": "Use SQL DB for user tweets (write path). For home timeline, use fanout approach: when user tweets, push to all followers' timeline caches (Redis lists). Store media in object store. For search, use a search cluster (Lucene) with scatter-gather. Fanout is O(n) per tweet - for celebrities with millions of followers, avoid fanout and instead merge their tweets at read time. Use: load balancers, CDN, memory cache for hot timelines, SQL read replicas, message queues for async notifications. Scale DB with federation/sharding.",
            "difficulty": "Hard"
        },
        {
            "topic": "System Design",
            "question": "Design a web crawler. The system should crawl the web, detect duplicate content, and handle billions of pages.",
            "answer": "Start with a URL frontier (queue) seeded with initial URLs. Worker nodes fetch pages, extract links, and add new URLs to the frontier. Use a Bloom filter or URL set (in Redis) to avoid reprocessing URLs. Detect duplicate content via content fingerprinting (simhash). Store raw HTML in object store, processed content in DB. Use politeness policy via queues per domain. Key components: URL frontier (prioritized queue), fetch workers, content parser, dedup store, content storage. Scale horizontally with worker pools. Use consistent hashing for URL distribution.",
            "difficulty": "Hard"
        },
        {
            "topic": "System Design",
            "question": "Design Mint.com - a personal finance system that aggregates financial accounts, categorizes transactions, and provides analytics.",
            "answer": "Use a backend service that connects to financial institutions via OFX/SCAP protocols. Collect transaction data via scheduled batch jobs. Store raw transactions in SQL DB, user accounts, and budgets. Use a separate analytics DB (columnar store like Redshift) for reporting. Key components: account aggregation service (scheduled batch jobs), transaction categorization (ML model or rules engine), budget tracking service, alert/notification service. Scale the aggregation layer horizontally, use caching for dashboards, queue for async processing.",
            "difficulty": "Hard"
        },
        {
            "topic": "System Design",
            "question": "Design the data structures for a social network. Support user profiles, friend connections, news feed, and friend suggestions.",
            "answer": "Use a graph database (or adjacency lists in SQL/NoSQL) for the social graph. Store user profiles in a document store or SQL. For news feed, use a fanout-on-write approach with Redis lists for each user's timeline. For friend suggestions, use breadth-first search limited to 2-3 hops, or ML-based recommendations. Key data structures: adjacency list for friends, B-tree for user index, sorted sets for feed ranking. Scale with graph partitioning, consistent hashing for user data, read replicas for profile queries.",
            "difficulty": "Hard"
        },
        {
            "topic": "System Design",
            "question": "Design a key-value store for a search engine. Needs to be highly available, partition-tolerant, and handle billions of key-value pairs.",
            "answer": "Use consistent hashing to distribute data across nodes. Each key maps to a virtual node on the ring. Replicate data to N nodes for fault tolerance (quorum-based replication: W+R > N for consistency). Use gossip protocol for node membership. Use Merkle trees for anti-entropy (sync). Handle temporary failures with hinted handoff. Use a LSM-tree-based storage engine (like LevelDB/RocksDB) for efficient writes. Key components: coordinator node, storage nodes, cluster manager (ZooKeeper).",
            "difficulty": "Hard"
        },
        {
            "topic": "System Design",
            "question": "Design Amazon's sales ranking by category feature. Show popular products with near real-time ranking, updated as sales happen.",
            "answer": "Use a stream processing approach. Sales events are published to a message queue (Kafka). A stream processor (Samza/Flink) aggregates sales counts per product per category in sliding windows (1hr, 24hr, 7d). Store rankings in Redis sorted sets for fast reads. Use a materialized view pattern: stream processor updates ranking caches. Components: Kafka for event ingestion, stream processor for aggregation, Redis for ranking cache, SQL DB for product metadata. Scale with partitioning by category.",
            "difficulty": "Hard"
        },
        {
            "topic": "System Design",
            "question": "Design a system that scales to millions of users on AWS. Start from a single-server setup and evolve.",
            "answer": "Phase 1: Single server with SQL DB, all in one. Phase 2: Separate web server from DB server. Phase 3: Add a web server, use load balancer (ELB), add read replicas for DB. Phase 4: Add CDN (CloudFront) for static assets, cache layer (ElastiCache). Phase 5: Make web tier stateless, move sessions to ElastiCache. Phase 6: Add auto-scaling groups for web tier. Phase 7: Read replicas for DB, shard writes. Phase 8: Use S3 for user content. Phase 9: Add message queues (SQS) for async processing. Phase 10: Microservices architecture with ECS/Kubernetes.",
            "difficulty": "Hard"
        },
    ]
    print(f"  Added {len(questions)} system design questions")
    return questions


def get_oop_design_questions():
    """Return OOP design questions from system-design-primer."""
    print("\n=== Adding OOP design questions ===")
    questions = [
        {
            "topic": "System Design",
            "question": "Design a hash map from scratch. Consider hash function, collision resolution, resizing, and thread safety.",
            "answer": "Implement with an array of buckets. Use a good hash function (e.g., DJB2 or FNV-1) to compute bucket index from key. For collision resolution, use separate chaining (linked list per bucket) or open addressing (linear/quadratic probing). Maintain a load factor threshold (0.75). When exceeded, resize the array (double size) and rehash all entries. For thread safety, use mutex locks or concurrent hash map techniques (striped locking). Time: O(1) average for get/put, O(n) worst case. Space: O(n).",
            "difficulty": "Medium"
        },
        {
            "topic": "System Design",
            "question": "Design a Least Recently Used (LRU) cache. Support get(key) and put(key, value) operations in O(1) time.",
            "answer": "Use a doubly linked list + hash map combination. The hash map maps keys to list nodes. The linked list maintains access order: most recently used items at the head, least recently used at the tail. get(): look up key in map, move node to head, return value. put(): if key exists, update value and move to head; if new, add node at head, if over capacity remove tail node and its map entry. Thread-safe version needs locks. Python: use collections.OrderedDict. Java: use LinkedHashMap.",
            "difficulty": "Medium"
        },
        {
            "topic": "System Design",
            "question": "Design a parking lot system. Handle multiple levels, parking spots of different sizes (compact, large, handicapped), and track availability.",
            "answer": "Use object-oriented design: ParkingLot (singleton) has multiple Levels. Each Level has multiple ParkingSpots (rows). ParkingSpot has type (compact/large/handicapped), status (occupied/available), and assigned Vehicle. Vehicle is abstract with Car, Motorcycle, Bus subclasses. ParkingLot.getAvailableSpot(vehicleType) finds nearest spot. assignSpot(vehicle, spot) marks spot occupied. removeVehicle(spot) frees it. Use a strategy pattern for spot assignment (nearest to exit, first available).",
            "difficulty": "Medium"
        },
        {
            "topic": "System Design",
            "question": "Design a call center system with multiple levels of employees (respondent, manager, director). Calls should be dispatched to the first available employee at the appropriate level.",
            "answer": "Use Chain of Responsibility pattern. CallCenter has a dispatchCall() method that assigns calls. Employee is abstract with Respondent, Manager, Director subclasses. Each employee has a rank and a handleCall() method. When a call comes in, dispatch to the lowest-ranked free employee. If they can't handle it, escalate to the next level. Use a queue per employee level (respondentQueue, managerQueue). Dispatch assigns calls from queues to free employees using round-robin or availability-first strategy.",
            "difficulty": "Medium"
        },
        {
            "topic": "System Design",
            "question": "Design a deck of cards. Support shuffle, deal, and comparison operations for card games.",
            "answer": "Card class has suit (Hearts, Diamonds, Clubs, Spades) and rank (2-10, J, Q, K, A). Deck contains 52 Card objects. shuffle() uses Fisher-Yates algorithm (O(n)). dealOneCard() returns the top card (removes from deck). DealHand(n) returns n cards. For specific games, use inheritance: BlackjackHand extends Hand with getScore(), PokerHand has isFlush(), isStraight(), etc. Considerations: immutable Card objects, factory pattern for standard decks, comparator interface for sorting.",
            "difficulty": "Medium"
        },
        {
            "topic": "System Design",
            "question": "Design a chat server. Support multiple chat rooms, private messaging, and online/offline status.",
            "answer": "Use a client-server architecture with WebSockets for persistent connections. User class has id, name, status (online/offline/away). ChatRoom has roomId, list of participants, message history. Message has senderId, timestamp, content, type (text/image/system). Private messaging uses direct 1-1 channels. Server handles: authentication, connection management, message routing, presence notification. Scale with multiple chat server instances behind a load balancer, Redis pub/sub for cross-server message routing, and a message queue for persistence.",
            "difficulty": "Medium"
        },
    ]
    print(f"  Added {len(questions)} OOP design questions")
    return questions


def get_backend_questions():
    """Return curated backend questions from arialdomartini's repo with answers."""
    print("\n=== Adding backend interview questions ===")
    questions = [
        {
            "topic": "System Design",
            "question": "Why are global and static objects considered evil in software design? Can you show it with a code example?",
            "answer": "Global/static objects introduce hidden shared state, making code hard to test, reason about, and parallelize. Example: a static Logger instance used across modules creates implicit coupling - changing the logger affects all consumers. Any test that uses a global object requires cleaning up state between tests. Global state also makes it impossible to have multiple isolated instances (e.g., for multi-tenant apps). Solution: use dependency injection to pass dependencies explicitly, making them visible and swappable.",
            "difficulty": "Medium"
        },
        {
            "topic": "System Design",
            "question": "What is Inversion of Control and how does it improve code design?",
            "answer": "IoC means inverting the flow of control - instead of your code controlling the flow (e.g., creating dependencies), the framework/container does. Hollywood Principle: 'Don't call us, we'll call you.' Benefits: decoupling (code depends on abstractions, not concretions), testability (dependencies can be mocked), reusability, and flexibility to swap implementations. Examples: Spring's DI container, JSF, plugin architectures.",
            "difficulty": "Medium"
        },
        {
            "topic": "System Design",
            "question": "What is the Law of Demeter (Principle of Least Knowledge)? Write code violating it and then fix it.",
            "answer": "Law of Demeter: a unit should only talk to its immediate friends (don't talk to strangers). Bad: order.getCustomer().getAddress().getZipCode() - this touches 3 objects deep. The Order class knows about Customer, Address, AND ZipCode internals. Fix: add order.getCustomerZipCode() which delegates internally. Better: order.getShippingZipCode() which encapsulates the entire concept. The fix reduces coupling - internal changes to how address is stored don't ripple through all callers.",
            "difficulty": "Medium"
        },
        {
            "topic": "System Design",
            "question": "Discuss Active Record vs Data Mapper patterns. When would you use each?",
            "answer": "Active Record: each object directly wraps a DB row and includes save/update/delete methods (e.g., Ruby on Rails). Simple but violates Single Responsibility - a class handles both business logic and persistence. Data Mapper: separates business objects from persistence (e.g., Hibernate, Entity Framework). Objects are pure business logic; a separate mapper layer handles DB operations. Use Active Record for simple CRUD apps or prototypes. Use Data Mapper for complex domains with rich business logic, for systems needing different persistence strategies, or when testing without a database.",
            "difficulty": "Medium"
        },
        {
            "topic": "System Design",
            "question": "Why is null often called a 'billion-dollar mistake' and what techniques avoid the problems it causes?",
            "answer": "Tony Hoare invented the null reference and called it a 'billion-dollar mistake' because it causes innumerable errors, vulnerabilities, and system crashes. NullPointerException/NullReferenceException is the most common runtime error. Techniques to avoid null: 1) Null Object Pattern - use a special no-op implementation instead of null. 2) Optional/Option types (Java Optional, Rust Option, Scala Option) encode emptiness in the type system. 3) Maybe monads in functional languages. 4) Use empty collections instead of null collections. 5) @Nullable/@NonNull annotations with static analysis.",
            "difficulty": "Medium"
        },
        {
            "topic": "System Design",
            "question": "In Object-Oriented Programming, why is composition often preferred over inheritance?",
            "answer": "Composition is preferred because: 1) It's more flexible - you can change behavior at runtime by swapping components. 2) Avoids the fragile base class problem - changes to a base class can break subclasses. 3) No deep hierarchical coupling - composition uses has-a relationships instead of is-a. 4) Easier to test - components can be mocked individually. 5) Follows the Open/Closed principle better. Use inheritance only for true is-a relationships where Liskov Substitution holds and the hierarchy is stable (e.g., Shape -> Circle).",
            "difficulty": "Medium"
        },
        {
            "topic": "System Design",
            "question": "What is an Anti-corruption Layer?",
            "answer": "An Anti-corruption Layer (ACL) is a boundary layer that translates between two different domain models or systems. It prevents one system's concepts from 'corrupting' another's by isolating translations. Common use: when integrating a legacy system with a modern one, the ACL sits between them and translates calls/data. Example: a microservice's domain objects differ from a legacy mainframe's models - the ACL handles all translations so neither side needs to change. It typically consists of adapters, facades, and translators.",
            "difficulty": "Medium"
        },
        {
            "topic": "System Design",
            "question": "What is the CAP theorem? Give examples of CP, AP, and CA systems.",
            "answer": "CAP theorem states that a distributed system can only provide two of three guarantees: Consistency (every read returns the latest write), Availability (every request gets a response), and Partition Tolerance (system works despite network failures). Since partitions are inevitable, you choose CP or AP. CP examples: traditional RDBMS with two-phase commit, ZooKeeper, HBase. AP examples: Cassandra, CouchDB, Amazon DynamoDB. CA is only possible in a single-node system (no partitions). In practice: most systems are CP or AP, with tunable consistency levels.",
            "difficulty": "Medium"
        },
        {
            "topic": "System Design",
            "question": "What is eventual consistency? When would you use it?",
            "answer": "Eventual consistency means that after a write, all reads will eventually see it (typically within milliseconds), but not immediately. Data is replicated asynchronously. DNS and email use eventual consistency. It's appropriate for: highly available systems where perfect consistency isn't critical, social media feeds (you don't mind if a post appears slightly delayed), content delivery networks. Trade-off: you accept temporary inconsistency for better availability and performance. Design accordingly with conflict resolution strategies (last-write-wins, CRDTs, etc.).",
            "difficulty": "Medium"
        },
        {
            "topic": "System Design",
            "question": "What's the difference between REST and SOAP? When would you choose one over the other?",
            "answer": "REST (Representational State Transfer) is an architectural style using HTTP methods (GET/POST/PUT/DELETE) with JSON/XML payloads. It's stateless, cacheable, and resource-oriented. SOAP (Simple Object Access Protocol) is a protocol with strict XML message formats and built-in error handling, security (WS-Security), and ACID transactions. Choose REST for: public APIs, mobile apps, microservices, CRUD operations, and when simplicity and performance matter. Choose SOAP for: enterprise systems requiring formal contracts, banking/financial apps needing built-in security, legacy integration, and ACID transactions across services.",
            "difficulty": "Medium"
        },
        {
            "topic": "System Design",
            "question": "What is a race condition? Provide an example and explain how to fix it.",
            "answer": "A race condition occurs when the behavior of software depends on the timing of uncontrollable events like thread scheduling. Example: two threads simultaneously checking if a key exists in a cache, both find it's missing, both compute the value, and both write it - wasting computation and potentially corrupting data. Fix: use synchronization (mutex/lock) around the check-and-set operation, or use atomic operations. Better: use a concurrent-safe cache implementation (e.g., Java's ConcurrentHashMap.computeIfAbsent) that handles this atomically.",
            "difficulty": "Medium"
        },
        {
            "topic": "System Design",
            "question": "What is ACID in databases? Explain each property.",
            "answer": "ACID stands for: Atomicity - a transaction is all-or-nothing; if any part fails, the entire transaction rolls back. Consistency - a transaction brings the database from one valid state to another, maintaining all defined rules (constraints, cascades, triggers). Isolation - concurrent transactions produce the same result as if they were executed sequentially. Isolation levels: Read Uncommitted, Read Committed, Repeatable Read, Serializable. Durability - once committed, a transaction's changes persist even after system failure (via write-ahead logging). ACID is the foundation of reliable transactional systems.",
            "difficulty": "Easy"
        },
        {
            "topic": "System Design",
            "question": "What is the N+1 query problem in ORMs and how do you fix it?",
            "answer": "The N+1 problem occurs when code loads a parent entity and then lazily loads N related child entities, resulting in 1 + N queries. Example: loading 100 blog posts (1 query) then accessing each post's author triggers 100 more queries. Fix: use eager loading (JOIN FETCH in JPA, .include() in Rails, select_related in Django) to load related entities in a single query with JOINs. Or use batch loading (eager load N entities at a time). Most ORMs support some form of eager loading or batch fetching.",
            "difficulty": "Easy"
        },
        {
            "topic": "System Design",
            "question": "What is the difference between scale-up and scale-out? When would you use each?",
            "answer": "Scale-up (vertical scaling) means adding more power to a single server (more CPU, RAM, faster disk). Simpler but has hard limits and becomes exponentially expensive. Scale-out (horizontal scaling) means adding more servers to distribute load. More complex but theoretically unlimited and uses commodity hardware. Use scale-up for: stateful services that are hard to distribute, databases (before sharding), legacy apps, simple deployments with low traffic. Use scale-out for: stateless web/app tiers, microservices, cloud-native apps, systems needing high availability and fault tolerance.",
            "difficulty": "Easy"
        },
        {
            "topic": "System Design",
            "question": "What is CQRS (Command Query Responsibility Segregation)?",
            "answer": "CQRS separates read and write operations into different models. Commands (writes) use a different model than Queries (reads). This allows optimizing each independently: the read model can be denormalized for fast queries, the write model can enforce business rules strictly. Benefits: independent scaling of reads vs writes, optimized data structures per operation, better security (different permissions for commands vs queries). Challenges: eventual consistency between models, increased complexity. Often used with Event Sourcing.",
            "difficulty": "Hard"
        },
        {
            "topic": "System Design",
            "question": "What is a deadlock? Give an example and explain prevention strategies.",
            "answer": "A deadlock occurs when two or more threads are waiting indefinitely for resources held by each other. Example: Thread A holds lock 1 and waits for lock 2; Thread B holds lock 2 and waits for lock 1. Neither can proceed. Four necessary conditions: Mutual Exclusion, Hold and Wait, No Preemption, Circular Wait. Prevention: 1) Lock ordering - always acquire locks in the same global order. 2) Use a timeout on lock acquisition. 3) Use tryLock() with backoff. 4) Use higher-level concurrency utilities (queues, executors) instead of raw locks. Detection: use lock ordering tools like ThreadMXBean in Java.",
            "difficulty": "Medium"
        },
        {
            "topic": "System Design",
            "question": "What is SQL injection? How do you prevent it?",
            "answer": "SQL injection is an attack where malicious SQL statements are inserted into input fields, tricking the application into executing unintended commands. Example: '; DROP TABLE users; --' as a username. Prevention: 1) Use parameterized queries/prepared statements (NEVER concatenate user input into SQL). 2) Use an ORM that handles escaping. 3) Validate and sanitize all inputs. 4) Apply the principle of least privilege on DB accounts. 5) Use stored procedures (with caution). 6) Use a web application firewall (WAF). Parameterized queries are the most effective defense.",
            "difficulty": "Easy"
        },
        {
            "topic": "System Design",
            "question": "What is two-factor authentication and how would you implement it?",
            "answer": "2FA adds a second verification layer beyond password (something you know). Second factor types: something you have (phone, hardware token), something you are (fingerprint, face). Implementation: 1) First factor: verify username/password normally. 2) Generate a one-time code (TOTP using time-based HMAC, or HOTP using counter). 3) Deliver via authenticator app (Google Authenticator), SMS, or email. 4) On login, prompt for code after password verification. 5) Verify the code server-side (check TOTP window ±30 seconds). Store a backup code for recovery.",
            "difficulty": "Medium"
        },
        {
            "topic": "System Design",
            "question": "How does HTTPS work? What's the role of TLS/SSL?",
            "answer": "HTTPS = HTTP over TLS/SSL. The TLS handshake: 1) Client sends 'ClientHello' with supported cipher suites and TLS version. 2) Server responds with 'ServerHello', its certificate (signed by a CA), and chosen cipher. 3) Client verifies the certificate against trusted CAs. 4) Client generates a random pre-master secret, encrypts it with the server's public key, sends it. 5) Both derive the session key from the pre-master secret. 6) They switch to symmetric encryption for the session. HTTPS protects against: eavesdropping (encryption), tampering (integrity via MACs), impersonation (certificate validation).",
            "difficulty": "Medium"
        },
        {
            "topic": "System Design",
            "question": "What's the difference between microservices and SOA?",
            "answer": "SOA (Service-Oriented Architecture) and microservices both decompose apps into services. Key differences: SOA uses an enterprise service bus (ESB) for communication, often with complex protocols (SOAP, WS-*). Microservices use lightweight protocols (HTTP/REST, gRPC, messaging). SOA services often share data stores, microservices have their own databases (database-per-service). SOA emphasizes service reuse across the enterprise, microservices emphasize bounded contexts and independent deployability. SOA services are typically larger ('macroservices'), microservices are smaller, more granular.",
            "difficulty": "Medium"
        },
    ]
    print(f"  Added {len(questions)} backend questions")
    return questions


def get_ml_questions():
    """Return ML interview questions from khangich's repo."""
    print("\n=== Adding ML interview questions ===")
    questions = [
        {
            "topic": "Machine Learning",
            "question": "Given that Alice has 2 kids, at least one of which is a girl, what is the probability that both kids are girls?",
            "answer": "The sample space for two children is: {BB, BG, GB, GG}. Given at least one is a girl, we eliminate BB, leaving {BG, GB, GG}. The probability of both being girls (GG) is 1/3. This is a classic conditional probability problem (similar to the 'Tuesday boy' problem). The answer would be different if we knew the older child was a girl (then the probability is 1/2 for the second child).",
            "difficulty": "Medium"
        },
        {
            "topic": "Machine Learning",
            "question": "Given an unfair coin where P(heads) != 0.5, design an algorithm to generate fair random bits (equal probability of 0 and 1).",
            "answer": "Von Neumann's method: Flip the coin twice. If you get HT, output 0. If you get TH, output 1. If you get HH or TT, discard and flip again. This works because even with a biased coin, P(HT) = P(TH) = p(1-p). The probability of HT equals TH regardless of the bias, as long as flips are independent. Efficiency: expected 2/(2p(1-p)) flips per output bit. This can be extended to generate uniform random numbers.",
            "difficulty": "Medium"
        },
        {
            "topic": "Machine Learning",
            "question": "A group of 60 students is randomly split into 3 classes of equal size (20 each). What is the probability that Jack and Jill end up in the same class?",
            "answer": "Place Jack in any class. Then there are 59 remaining slots, and 19 of them are in Jack's class (since each class has 20 students). The probability Jill is in Jack's class is 19/59 ≈ 0.322. Alternatively: total ways to partition = 60!/(20!)^3. Ways they're together: pick class (3 choices), then place them both there (18 remaining slots for that class) = 3 * 58!/(20! * 20! * 18!). The ratio gives 19/59.",
            "difficulty": "Medium"
        },
        {
            "topic": "Machine Learning",
            "question": "What is the difference between L1 and L2 regularization? When would you use each?",
            "answer": "L1 (Lasso) adds sum of absolute weights as penalty, L2 (Ridge) adds sum of squared weights. L1 drives weights to exactly zero (feature selection), L2 shrinks weights but doesn't eliminate them. L1 is useful when you expect sparse features (many irrelevant). L2 is better when all features are somewhat relevant. L1 handles outliers better, L2 is more stable. L1 solution isn't differentiable at zero (needs subgradient methods). Elastic Net combines both. From Bayesian perspective: L1 = Laplace prior, L2 = Gaussian prior.",
            "difficulty": "Medium"
        },
        {
            "topic": "Machine Learning",
            "question": "Explain the difference between Random Forest and Gradient Boosting (GBDT/XGBoost).",
            "answer": "Both are ensemble tree methods. Random Forest builds many decision trees independently in parallel, each on a bootstrap sample with random feature subsets, then averages predictions. This reduces variance. Gradient Boosting builds trees sequentially, each correcting the errors of the previous ensemble. This reduces bias. RF is simpler, fewer hyperparameters, handles outliers better, and is hard to overfit. Boosting typically achieves higher accuracy but requires careful tuning (learning rate, tree depth) and can overfit. XGBoost/LightGBM add regularization and optimization for practical superiority.",
            "difficulty": "Medium"
        },
        {
            "topic": "Machine Learning",
            "question": "What is the bias-variance tradeoff?",
            "answer": "Bias is the error from wrong assumptions in the learning algorithm (underfitting - too simple). Variance is the error from sensitivity to small fluctuations in the training set (overfitting - too complex). The tradeoff: as model complexity increases, bias decreases but variance increases. Total error = bias^2 + variance + irreducible error. Goal is to find the sweet spot that minimizes total error. Techniques to manage: cross-validation for model selection, regularization (L1/L2), ensemble methods (bagging reduces variance, boosting reduces bias).",
            "difficulty": "Medium"
        },
        {
            "topic": "Machine Learning",
            "question": "What is the difference between generative and discriminative models? Give examples.",
            "answer": "Generative models learn P(X,Y) - the joint probability distribution - and can generate new data samples. They model how the data is generated. Discriminative models learn P(Y|X) - the conditional probability - directly mapping inputs to outputs. Examples of generative: Naive Bayes, Gaussian Mixture Models, Hidden Markov Models, GANs, VAEs. Examples of discriminative: Logistic Regression, SVMs, Neural Networks, Random Forests. Generative models can handle missing data, detect outliers, and generate samples, but typically require more data. Discriminative models usually achieve higher accuracy on classification tasks.",
            "difficulty": "Medium"
        },
        {
            "topic": "Machine Learning",
            "question": "Explain how backpropagation works in neural networks.",
            "answer": "Backpropagation computes gradients of the loss function with respect to network weights using the chain rule. Steps: 1) Forward pass - compute predictions and loss. 2) Compute gradient of loss w.r.t. output layer activations. 3) Propagate error backwards through the network: for each layer, compute gradient of loss w.r.t. weights using the chain rule (∂L/∂w = ∂L/∂a * ∂a/∂z * ∂z/∂w where a=activation, z=weighted input). 4) Update weights using gradient descent: w = w - η * ∂L/∂w. Key concepts: vanishing/exploding gradients, activation function derivatives, mini-batch processing. Modern frameworks handle this automatically via automatic differentiation.",
            "difficulty": "Hard"
        },
        {
            "topic": "Machine Learning",
            "question": "What is the difference between bagging and boosting?",
            "answer": "Bagging (Bootstrap Aggregating) trains multiple models in parallel on different bootstrap samples of the data and averages their predictions. Reduces variance. Example: Random Forest. Boosting trains models sequentially, each focusing on the mistakes of previous models by adjusting sample weights. Reduces bias but can increase variance. Examples: AdaBoost, Gradient Boosting, XGBoost. Bagging is simpler and parallelizable, boosting typically achieves higher accuracy but risks overfitting if not tuned properly. Both are ensemble methods that combine weak learners into strong ones.",
            "difficulty": "Easy"
        },
        {
            "topic": "Machine Learning",
            "question": "What is PCA (Principal Component Analysis)? How does it work?",
            "answer": "PCA is an unsupervised dimensionality reduction technique. Steps: 1) Standardize the data (zero mean, unit variance). 2) Compute the covariance matrix. 3) Compute eigenvectors and eigenvalues of the covariance matrix. 4) Sort eigenvectors by decreasing eigenvalues. 5) Select top k eigenvectors as principal components. 6) Project data onto the selected components. PCA finds the directions of maximum variance in the data. Use cases: visualization (2D/3D), noise reduction, feature extraction, preprocessing before other ML algorithms. Limitations: linear, assumes orthogonality, sensitive to scaling.",
            "difficulty": "Medium"
        },
        {
            "topic": "Machine Learning",
            "question": "What is SMOTE? When would you use it?",
            "answer": "SMOTE (Synthetic Minority Oversampling TEchnique) is used to handle class imbalance. Instead of simply duplicating minority class samples, SMOTE creates synthetic samples by interpolating between existing minority instances. Steps: 1) For each minority sample, find its k nearest neighbors (same class). 2) Randomly select one of these neighbors. 3) Create a synthetic sample at a random point along the line between the sample and its neighbor. Use SMOTE when you have imbalanced classification problems (e.g., fraud detection with 99.9% legitimate, 0.1% fraudulent). Combine with undersampling of majority class.",
            "difficulty": "Medium"
        },
    ]
    print(f"  Added {len(questions)} ML questions")
    return questions


def deduplicate_and_merge(existing_questions, new_questions):
    """Merge new questions into existing, deduplicating by question text similarity."""
    print("\n=== Deduplicating and merging ===")
    
    # Create a set of existing question fingerprints (lowercase, stripped)
    existing_texts = set()
    existing_topics = {}
    for q in existing_questions:
        key = q['question'].lower().strip()
        existing_texts.add(key)
        existing_topics.setdefault(q['topic'], 0)
        existing_topics[q['topic']] += 1
    
    print(f"  Existing: {len(existing_questions)} questions across {len(existing_topics)} topics")
    for t, c in sorted(existing_topics.items()):
        print(f"    {t}: {c}")
    
    # Filter new questions - skip if text already exists
    next_id = max(q['id'] for q in existing_questions) + 1 if existing_questions else 1
    
    added = 0
    skipped = 0
    for q in new_questions:
        key = q['question'].lower().strip()
        if key not in existing_texts:
            existing_texts.add(key)
            q['id'] = next_id
            next_id += 1
            existing_questions.append(q)
            added += 1
        else:
            skipped += 1
    
    print(f"  Added: {added} new questions")
    print(f"  Skipped (duplicates): {skipped}")
    return existing_questions


def main():
    print("=" * 60)
    print("INTERVIEW QUESTIONS PROCESSOR")
    print("=" * 60)
    
    # Load existing questions
    if os.path.exists(QUESTIONS_JSON):
        with open(QUESTIONS_JSON, 'r', encoding='utf-8') as f:
            existing = json.load(f)
        print(f"\nLoaded {len(existing)} existing questions")
    else:
        existing = []
        print("\nNo existing questions.json found, starting fresh")
    
    # Fetch new questions from all sources
    all_new = []
    
    try:
        q30 = fetch_30_seconds_questions()
        all_new.extend(q30)
    except Exception as e:
        print(f"Error fetching 30-seconds questions: {e}")
    
    try:
        sd = get_system_design_questions()
        all_new.extend(sd)
    except Exception as e:
        print(f"Error adding system design questions: {e}")
    
    try:
        oop = get_oop_design_questions()
        all_new.extend(oop)
    except Exception as e:
        print(f"Error adding OOP questions: {e}")
    
    try:
        be = get_backend_questions()
        all_new.extend(be)
    except Exception as e:
        print(f"Error adding backend questions: {e}")
    
    try:
        ml = get_ml_questions()
        all_new.extend(ml)
    except Exception as e:
        print(f"Error adding ML questions: {e}")
    
    print(f"\nTotal new questions from all sources: {len(all_new)}")
    
    # Merge and deduplicate
    merged = deduplicate_and_merge(existing, all_new)
    
    # Write back
    print(f"\nWriting {len(merged)} questions to {QUESTIONS_JSON}...")
    with open(QUESTIONS_JSON, 'w', encoding='utf-8') as f:
        json.dump(merged, f, indent=2, ensure_ascii=False)
    
    # Print final stats
    topics = {}
    for q in merged:
        topics[q['topic']] = topics.get(q['topic'], 0) + 1
    
    print("\n=== FINAL STATISTICS ===")
    print(f"Total questions: {len(merged)}")
    for t, c in sorted(topics.items()):
        print(f"  {t}: {c}")
    print("=" * 60)


if __name__ == '__main__':
    main()
