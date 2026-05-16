import json
import random

random.seed(42)

# ============================================================
# Spring Boot Troubleshooting Question Generator
# ============================================================

# --- SCENARIO TEMPLATES ---
# Each template has: question, answer, difficulty
# We'll generate variations with different contexts, configs, and specifics.

# ====== CATEGORY 1: Startup & Boot Issues ======
startup_scenarios = [
    {
        "question": "Spring Boot application fails to start with 'Port 8080 already in use' error in production. The previous instance was killed but port is still bound. How do you diagnose and resolve this?",
        "answer": "1) Run 'lsof -i :8080' or 'netstat -tulpn | grep 8080' to find the PID holding the port. 2) Kill the zombie process with 'kill -9 <PID>'. 3) If it's a Docker container, restart it. 4) Configure server.port=0 for random port in dev, or add server.shutdown=graceful in application.yml for clean shutdowns. 5) Add a startup health check script to CI/CD.",
        "difficulty": "Easy"
    },
    {
        "question": "Application throws 'BeanCreationException: Error creating bean with name X' during startup. The bean depends on a configuration class that reads from application.properties. What's your debugging approach?",
        "answer": "1) Check the full stack trace for the root cause - often a nested exception. 2) Verify the property key exists in application.properties/yml. 3) Check @Value or @ConfigurationProperties binding - typos in property names cause silent failures. 4) Use @ConditionalOnProperty to make the bean conditional. 5) Enable debug logging with 'logging.level.org.springframework=DEBUG' to see bean creation order. 6) Check for circular dependencies between beans.",
        "difficulty": "Medium"
    },
    {
        "question": "Spring Boot app startup takes 45+ seconds in production. Local startup is 8 seconds. What could cause this and how do you optimize?",
        "answer": "1) Enable startup tracking with 'spring.main.lazy-initialization=true' to defer bean creation. 2) Check DNS resolution delays - add '-Djava.net.preferIPv4Stack=true'. 3) Profile with Spring Boot Actuator's /actuator/startup endpoint. 4) Reduce component scan scope with specific @ComponentScan basePackages. 5) Use @Lazy on non-critical beans. 6) Check if database connection pool initialization is blocking - use lazy connection initialization. 7) Consider Spring Native/AOT for faster startup.",
        "difficulty": "Medium"
    },
    {
        "question": "After adding a new @Configuration class, the application fails to start with 'Circular reference involving bean X'. How do you break the cycle?",
        "answer": "1) Identify the circular dependency chain from the error message. 2) Use constructor injection refactoring - split beans so dependencies flow one direction. 3) Apply @Lazy on one of the constructor parameters as a quick fix. 4) Use setter or field injection for one side of the cycle (not preferred). 5) Create a third bean that both depend on instead of depending on each other. 6) Set 'spring.main.allow-circular-references=true' as a temporary workaround but plan to refactor.",
        "difficulty": "Medium"
    },
    {
        "question": "Spring Boot application fails to start in Docker container with exit code 137. The logs show nothing unusual before termination. What's happening?",
        "answer": "Exit code 137 means OOMKilled (128 + SIGKILL 9). 1) Check container memory limits with 'docker inspect'. 2) Increase JVM heap: '-Xmx512m -Xms256m' in JAVA_OPTS. 3) Set container memory limit higher than JVM max heap (JVM needs extra for metaspace, threads, native memory). 4) Use '-XX:+UseContainerSupport -XX:MaxRAMPercentage=75.0' for container-aware JVM. 5) Monitor with 'docker stats' during startup. 6) Check for memory leaks in application code.",
        "difficulty": "Medium"
    },
    {
        "question": "Application won't start after upgrading from Spring Boot 2.7 to 3.2. Error: 'NoSuchMethodError' in a third-party library. How do you resolve this?",
        "answer": "1) Identify the incompatible library from the stack trace. 2) Check the library's compatibility matrix with Spring Boot 3.x (requires Java 17+ and Jakarta EE namespace). 3) Update the dependency version in pom.xml/build.gradle. 4) Run 'mvn dependency:tree' or 'gradle dependencies' to find transitive conflicts. 5) Use <dependencyManagement> or platform BOM to enforce versions. 6) Replace javax.* imports with jakarta.* if migrating from Java EE. 7) Check Spring Boot migration guide for breaking changes.",
        "difficulty": "Hard"
    },
    {
        "question": "Spring Boot starts but immediately shuts down with 'No active profile set, falling back to 1 default profile'. No web server starts. What's wrong?",
        "answer": "1) Check if spring-boot-starter-web is in dependencies - missing it means no embedded server. 2) Verify the main class has @SpringBootApplication annotation. 3) Check if a @Component is throwing an exception during initialization that causes context close. 4) Look for 'spring.main.web-application-type=none' in config. 5) Enable debug logging to see full startup sequence. 6) Verify no other auto-configuration is excluding the web starter.",
        "difficulty": "Easy"
    },
    {
        "question": "After adding spring-boot-starter-actuator, the application fails to start with 'Multiple representations of the same entity X are being merged'. What's the conflict?",
        "answer": "1) This is typically a JPA/Hibernate issue, not directly actuator-related. 2) Check if actuator's /entities endpoint is exposing entities with lazy-loaded relationships. 3) Configure 'spring.jpa.open-in-view=false' to avoid lazy loading issues. 4) Use DTOs instead of exposing entities directly through actuator endpoints. 5) Check for duplicate entity manager configurations. 6) Review actuator endpoint exposure settings in application.properties.",
        "difficulty": "Hard"
    },
    {
        "question": "Spring Boot application fails on startup with 'Failed to configure a DataSource: no embedded datasource could be configured'. You don't need a database for this service. How do you fix it?",
        "answer": "1) Exclude DataSource auto-configuration: @SpringBootApplication(exclude = {DataSourceAutoConfiguration.class}). 2) Or set 'spring.autoconfigure.exclude=org.springframework.boot.autoconfigure.jdbc.DataSourceAutoConfiguration' in application.properties. 3) If using spring-boot-starter-data-jpa, exclude it or replace with spring-boot-starter-web only. 4) For specific configurations, use @ConditionalOnProperty to conditionally enable database beans.",
        "difficulty": "Easy"
    },
    {
        "question": "Application startup fails with 'Invalid bean definition with name X: Could not resolve placeholder Y in value Z'. The property exists in the config file. Why?",
        "answer": "1) Verify the property file is being loaded - check @PropertySource paths. 2) Check for typos in the placeholder key vs actual property name. 3) Ensure the config file is in the classpath (src/main/resources). 4) For external configs, verify the file path in '--spring.config.location'. 5) Check if the property is defined in a profile-specific file (application-dev.properties) but the profile isn't active. 6) Use @ConfigurationProperties as an alternative to @Value for better error messages.",
        "difficulty": "Medium"
    },
]

# ====== CATEGORY 2: Database & Connection Pool Issues ======
database_scenarios = [
    {
        "question": "Production Spring Boot app intermittently throws 'CannotGetJdbcConnectionException: Failed to obtain JDBC Connection'. The database is up and responsive. What's wrong?",
        "answer": "1) Check connection pool exhaustion - HikariCP default is 10 connections. 2) Monitor active connections: 'SELECT count(*) FROM pg_stat_activity' for PostgreSQL. 3) Look for connection leaks - connections not closed after use. 4) Increase pool size: 'spring.datasource.hikari.maximum-pool-size=20'. 5) Set connection timeout: 'spring.datasource.hikari.connection-timeout=30000'. 6) Enable leak detection: 'spring.datasource.hikari.leak-detection-threshold=60000'. 7) Ensure all repositories close connections properly - use try-with-resources.",
        "difficulty": "Medium"
    },
    {
        "question": "Spring Boot app with Hibernate throws 'LazyInitializationException: could not initialize proxy - no Session' when accessing a related entity in a REST controller. How do you fix this?",
        "answer": "1) Use @EntityGraph on the repository method to eagerly fetch the relationship: @EntityGraph(attributePaths = {'relatedEntity'}). 2) Use JOIN FETCH in JPQL: 'SELECT e FROM Entity e JOIN FETCH e.relatedEntity'. 3) Use DTO projection instead of returning entities. 4) Set 'spring.jpa.open-in-view=true' (not recommended for production). 5) Use @Transactional on the service method that accesses the lazy property. 6) Initialize the relationship before returning from the service layer.",
        "difficulty": "Medium"
    },
    {
        "question": "Database migration with Flyway fails on startup with 'Validate failed: Migrations have failed validation'. The migration scripts haven't changed. What could cause this?",
        "answer": "1) Check if someone manually modified the database schema outside Flyway. 2) Run 'flyway info' to see migration status and checksums. 3) If checksums differ, use 'flyway repair' to recalculate them (only if scripts truly match). 4) Check for out-of-order migrations - set 'spring.flyway.out-of-order=true' if needed. 5) Verify the migration file wasn't modified after being applied - Flyway stores checksums. 6) For hotfixes, create a new migration rather than modifying existing ones.",
        "difficulty": "Medium"
    },
    {
        "question": "Spring Boot JPA application shows 'org.hibernate.exception.LockAcquisitionException: could not execute statement' under concurrent load. How do you handle this?",
        "answer": "1) Implement retry logic with @Retryable from spring-retry. 2) Use optimistic locking with @Version field on entities. 3) For pessimistic locking, use 'SELECT ... FOR UPDATE' with @Lock(LockModeType.PESSIMISTIC_WRITE). 4) Reduce transaction scope - keep transactions as short as possible. 5) Set appropriate isolation level: 'spring.jpa.properties.hibernate.connection.isolation'. 6) Use database-specific deadlock detection and configure retry at the DB level. 7) Monitor with 'SHOW ENGINE INNODB STATUS' for MySQL deadlock info.",
        "difficulty": "Hard"
    },
    {
        "question": "After deploying a new version, the app throws 'org.hibernate.MappingException: Unknown entity: com.example.model.NewEntity'. The entity class exists and has @Entity annotation.",
        "answer": "1) Check if the entity package is included in @EntityScan or @ComponentScan. 2) Verify the @Entity import is 'jakarta.persistence.Entity' (Spring Boot 3) not 'javax.persistence.Entity'. 3) Check if the entity class is in a sub-package not scanned by Spring. 4) Run a clean build - stale class files can cause this. 5) Verify the entity is not excluded by any filter. 6) Check persistence.xml or hibernate.cfg.xml if using XML configuration. 7) Enable 'spring.jpa.show-sql=true' to see what Hibernate is scanning.",
        "difficulty": "Easy"
    },
    {
        "question": "Spring Boot app with multiple data sources throws 'Not a managed type: class com.example.Entity' for entities in the secondary datasource. How do you configure multi-datasource JPA?",
        "answer": "1) Create separate EntityManagerFactory beans for each datasource. 2) Use @EntityScan with specific basePackages for each EMF. 3) Configure separate LocalContainerEntityManagerFactoryBean with different persistence units. 4) Mark one datasource as @Primary. 5) Use separate repository packages with @EnableJpaRepositories(basePackages = '...') for each datasource. 6) Ensure each entity package is only scanned by one EMF - overlapping scans cause conflicts. 7) Use distinct transaction managers for each datasource.",
        "difficulty": "Hard"
    },
    {
        "question": "HikariCP connection pool shows 'Connection is not available, request timed out after 30000ms' during peak traffic. Increasing pool size doesn't help. What's the real issue?",
        "answer": "1) The issue is likely slow queries holding connections too long, not pool size. 2) Enable slow query logging in the database. 3) Use 'spring.datasource.hikari.leak-detection-threshold=30000' to find leaked connections. 4) Profile queries with 'spring.jpa.properties.hibernate.generate_statistics=true'. 5) Add missing database indexes - check query execution plans. 6) Implement query timeouts: 'spring.jpa.properties.hibernate.query.timeout=5000'. 7) Consider read replicas for read-heavy workloads. 8) Use connection pool metrics from Actuator's /actuator/metrics/hikaricp.connections.",
        "difficulty": "Hard"
    },
    {
        "question": "Spring Data JPA repository method 'findByStatusAndCreatedDateBetween' returns stale data. The database has newer records but the query returns old results.",
        "answer": "1) Check if Hibernate's first-level cache is returning cached entities - use entityManager.clear() or entityManager.detach(). 2) For second-level cache, verify cache eviction is working. 3) Add '@Modifying(clearAutomatically = true)' if this follows a modifying query. 4) Check transaction isolation level - READ_COMMITTED should see committed changes. 5) Verify the query parameters (date range) are correct - timezone issues can cause date mismatches. 6) Use 'entityManager.flush()' before querying if writes haven't been flushed. 7) Disable query result cache for this method if caching is enabled.",
        "difficulty": "Medium"
    },
]

# ====== CATEGORY 3: REST API & Web Layer Issues ======
rest_scenarios = [
    {
        "question": "Spring Boot REST API returns 415 Unsupported Media Type when posting JSON to an endpoint. The Content-Type header is set to 'application/json'. What's wrong?",
        "answer": "1) Verify @RequestBody annotation is on the controller method parameter. 2) Check that jackson-databind is on the classpath (included in spring-boot-starter-web). 3) Verify the request body JSON matches the DTO structure - mismatched field names cause deserialization failures. 4) Check for missing no-args constructor on the DTO. 5) Verify @PostMapping consumes MediaType.APPLICATION_JSON_VALUE. 6) Enable 'logging.level.org.springframework.web=DEBUG' to see the content negotiation process. 7) Check if a custom HttpMessageConverter is interfering.",
        "difficulty": "Easy"
    },
    {
        "question": "A @RestController endpoint returns a 500 Internal Server Error with 'HttpMessageNotWritableException: No converter found for return value of type'. The method returns a custom object.",
        "answer": "1) The object lacks a proper getter/setter or Jackson can't serialize it. 2) Add getters for all fields Jackson needs to serialize. 3) Add @JsonProperty annotations if field names don't match. 4) Check for circular references in the object graph - use @JsonIgnore or @JsonBackReference. 5) Ensure the class has a no-args constructor or use @JsonCreator. 6) Add 'jackson-module-kotlin' if using Kotlin data classes. 7) Test serialization in isolation with ObjectMapper.writeValueAsString().",
        "difficulty": "Medium"
    },
    {
        "question": "Spring Boot CORS configuration isn't working - browser blocks cross-origin requests despite adding @CrossOrigin on the controller. Preflight OPTIONS requests fail with 403.",
        "answer": "1) @CrossOrigin on controller may not cover all paths - use a global WebMvcConfigurer: addCorsMappings in a @Configuration class. 2) Check if Spring Security is intercepting OPTIONS requests - add '.requestMatchers(CorsUtils::isPreFlightRequest).permitAll()' in SecurityFilterChain. 3) Verify allowed origins include the requesting domain - '*' doesn't work with credentials. 4) Check if a filter before the CORS filter is blocking the request. 5) Enable CORS debug logging: 'logging.level.org.springframework.web.cors=DEBUG'. 6) For Spring Security 6+, configure cors() in the SecurityFilterChain bean.",
        "difficulty": "Hard"
    },
    {
        "question": "REST API endpoint with @Valid annotation on @RequestBody doesn't throw MethodArgumentNotValidException for invalid input. Validation is silently skipped.",
        "answer": "1) Verify 'spring-boot-starter-validation' is in dependencies (not included in starter-web since Boot 3). 2) Check that validation annotations (@NotNull, @NotBlank, etc.) are on the DTO fields. 3) Ensure @Valid is on the @RequestBody parameter, not the method. 4) Check if a custom Validator is overriding the default one. 5) Verify the DTO has getters - some validators need them. 6) Add a @ControllerAdvice with @ExceptionHandler(MethodArgumentNotValidException) to see validation errors. 7) Test with 'mvn dependency:tree' to ensure hibernate-validator is present.",
        "difficulty": "Medium"
    },
    {
        "question": "Spring Boot application returns dates in REST API as timestamps (numbers) instead of ISO-8601 strings. Frontend expects '2024-01-15T10:30:00' format.",
        "answer": "1) Set 'spring.jackson.serialization.write-dates-as-timestamps=false' in application.properties. 2) Add 'spring.jackson.date-format=yyyy-MM-dd'T'HH:mm:ss' for custom format. 3) Use @JsonFormat(pattern = 'yyyy-MM-dd'T'HH:mm:ss') on specific date fields. 4) Configure a global ObjectMapper bean with JavaTimeModule. 5) For LocalDateTime, ensure jackson-datatype-jsr310 is on classpath (included in starter-web). 6) Set 'spring.jackson.serialization.write-date-keys-as-timestamps=false'. 7) Consider timezone: 'spring.jackson.time-zone=UTC'.",
        "difficulty": "Easy"
    },
    {
        "question": "File upload endpoint with MultipartFile fails with 'MaxUploadSizeExceededException' for files larger than 1MB. You've set 'spring.servlet.multipart.max-file-size=50MB' but it's still rejecting.",
        "answer": "1) Check if there's a reverse proxy (Nginx, Apache) with its own size limit - set 'client_max_body_size 50m' in Nginx. 2) Verify both max-file-size AND max-request-size are set: 'spring.servlet.multipart.max-request-size=50MB'. 3) If behind a load balancer, check its body size limit. 4) For Spring Security, ensure the multipart filter is configured before security filters. 5) Check Tomcat's max-swallow-size if using embedded Tomcat. 6) Add a @ControllerAdvice to handle MaxUploadSizeExceededException gracefully with a proper error response.",
        "difficulty": "Medium"
    },
    {
        "question": "Spring Boot REST API with pagination returns wrong total count - Page.getTotalElements() shows fewer records than actually exist in the database.",
        "answer": "1) Check if the query has JOINs causing duplicate rows - use 'SELECT DISTINCT' or 'count(DISTINCT e.id)'. 2) For Spring Data JPA, use 'PageableExecutionUtils' or a separate count query with @Query(countQuery = '...'). 3) Verify the count query isn't being affected by the same JOINs as the data query. 4) Check if soft-delete filters (@Where) are affecting the count differently. 5) Use 'setDistinct(true)' on the CriteriaQuery. 6) Test the count query separately in the database to verify correctness. 7) Consider using 'Slice' instead of 'Page' if you only need next-page info.",
        "difficulty": "Hard"
    },
    {
        "question": "Spring Boot API returns 200 OK for error scenarios instead of proper HTTP error codes. The controller catches exceptions and returns ResponseEntity with wrong status.",
        "answer": "1) Implement a global @ControllerAdvice with @ExceptionHandler for consistent error handling. 2) Map specific exceptions to HTTP status codes: @ExceptionHandler(ResourceNotFoundException.class) -> ResponseEntity.notFound(). 3) Use @ResponseStatus on custom exception classes. 4) Avoid catching generic Exception in controllers - let the global handler manage it. 5) Return ResponseEntity<ErrorResponse> with proper status, message, and timestamp. 6) Use ProblemDetail (Spring Boot 3) for RFC 7807 compliant error responses. 7) Test error paths with @WebMvcTest and MockMvc.",
        "difficulty": "Medium"
    },
]

# ====== CATEGORY 4: Security & Authentication Issues ======
security_scenarios = [
    {
        "question": "After adding spring-boot-starter-security, all endpoints return 403 Forbidden including public ones. The generated password in logs doesn't work for login.",
        "answer": "1) Spring Security locks down all endpoints by default - configure a SecurityFilterChain bean to permit public paths. 2) Use 'http.authorizeHttpRequests(auth -> auth.requestMatchers('/public/**', '/actuator/health').permitAll().anyRequest().authenticated())'. 3) For the login issue, the default user is 'user' with the generated password. 4) Override with 'spring.security.user.name' and 'spring.security.user.password' in application.properties. 5) For Spring Security 6+, the configuration style changed from WebSecurityConfigurerAdapter to SecurityFilterChain beans. 6) Check if CSRF is blocking POST requests - disable for APIs: 'http.csrf(csrf -> csrf.disable())'.",
        "difficulty": "Medium"
    },
    {
        "question": "JWT authentication works locally but fails in production with 'io.jsonwebtoken.ExpiredJwtException'. The token expiry is set to 24 hours and was just issued.",
        "answer": "1) Check server time synchronization - production server clock may be ahead. Use NTP to sync time. 2) Verify the JWT signing key is the same across instances - different keys cause validation failures. 3) Check timezone differences between issuing and validating servers. 4) Add a clock skew tolerance: 'Jwts.parser().setAllowedClockSkewSeconds(60)'. 5) Verify the token isn't being cached with stale values. 6) Check if load balancer is stripping or modifying Authorization headers. 7) Log the token's 'exp' claim to verify actual expiry time.",
        "difficulty": "Hard"
    },
    {
        "question": "Spring Security OAuth2 login with Google works in development but returns 'redirect_uri_mismatch' in production. The redirect URI in Google Console matches the production URL.",
        "answer": "1) Check for trailing slash differences - 'https://example.com/login/oauth2/code/google' vs 'https://example.com/login/oauth2/code/google/'. 2) Verify the scheme (http vs https) matches exactly. 3) Check if a reverse proxy is changing the redirect URI - set 'server.forward-headers-strategy=native'. 4) For Spring Boot behind a proxy, configure 'server.use-forward-headers=true'. 5) Verify the OAuth2 client registration in application.yml matches the Google Console configuration. 6) Check if the production URL has a different port or path prefix. 7) Enable debug logging: 'logging.level.org.springframework.security=DEBUG'.",
        "difficulty": "Hard"
    },
    {
        "question": "Spring Boot application with Spring Security allows unauthenticated access to /admin endpoints despite having '.requestMatchers('/admin/**').hasRole('ADMIN')' configured.",
        "answer": "1) Check the order of matcher rules - 'anyRequest().permitAll()' before the admin rule would override it. 2) Remember 'hasRole('ADMIN')' checks for 'ROLE_ADMIN' - the 'ROLE_' prefix is auto-added. 3) Verify the user actually has the ADMIN role assigned in your UserDetailsService. 4) Check if there's a conflicting SecurityFilterChain bean with lower @Order that permits access. 5) Use 'hasAuthority('ROLE_ADMIN')' instead if roles aren't working. 6) Test with '@WithMockUser(roles = 'ADMIN')' in unit tests. 7) Enable security debug logging to trace the authorization decision.",
        "difficulty": "Medium"
    },
    {
        "question": "CSRF protection is blocking legitimate POST requests from a mobile app to the Spring Boot API. Disabling CSRF entirely feels insecure.",
        "answer": "1) CSRF is only needed for browser-based sessions with cookies - mobile apps using tokens don't need it. 2) Configure CSRF to only apply to session-based auth: 'http.csrf(csrf -> csrf.csrfTokenRepository(CookieCsrfTokenRepository.withHttpOnlyFalse()).requireCsrfProtectionMatcher(new AntPathRequestMatcher('/api/**', 'POST').negate()))'. 3) Better: disable CSRF for stateless API endpoints: 'http.securityMatcher('/api/**').csrf(csrf -> csrf.disable())'. 4) Keep CSRF enabled for form-based login pages. 5) Use separate SecurityFilterChain beans: one for web (with CSRF) and one for API (without). 6) For mobile apps, use token-based auth (JWT) which is inherently CSRF-safe.",
        "difficulty": "Hard"
    },
    {
        "question": "Spring Boot app with Spring Security throws 'InsufficientAuthenticationException' when accessing /actuator endpoints despite having proper roles configured.",
        "answer": "1) Actuator endpoints have their own security configuration separate from main app security. 2) Configure 'management.endpoints.web.exposure.include=*' to expose endpoints. 3) Set 'management.endpoint.health.show-details=always' for health details. 4) For actuator-specific security, configure a separate SecurityFilterChain with 'http.securityMatcher('/actuator/**')'. 5) Or use 'management.endpoints.web.base-path=/manage' to isolate actuator paths. 6) Set 'spring.boot.admin.client.instance.metadata.user.name' for Spring Boot Admin. 7) Consider using a separate management port: 'management.server.port=8081'.",
        "difficulty": "Medium"
    },
]

# ====== CATEGORY 5: Microservices & Distributed Systems ======
microservices_scenarios = [
    {
        "question": "Spring Boot microservice using RestTemplate to call another service gets 'Connection refused' intermittently. The target service is running and healthy.",
        "answer": "1) Check if the target service's pod/container is being restarted - use Kubernetes readiness probes. 2) Implement retry logic with Spring Retry: @Retryable(maxAttempts = 3, backoff = @Backoff(delay = 1000)). 3) Use a circuit breaker with Resilience4j to fail fast when the service is down. 4) Check DNS resolution delays in the cluster. 5) Verify the service URL is correct - use service discovery (Eureka/Consul) instead of hardcoded URLs. 6) Add connection pooling to RestTemplate with PoolingHttpClientConnectionManager. 7) Consider migrating to WebClient (reactive) or Feign client for better resilience.",
        "difficulty": "Medium"
    },
    {
        "question": "Spring Cloud Config Server returns stale configuration values after updating the Git repo. Services don't pick up the new config even after restart.",
        "answer": "1) Verify the Config Server is pulling from the correct branch - check 'spring.cloud.config.server.git.uri' and 'default-label'. 2) Use '/actuator/refresh' endpoint to refresh config at runtime (with @RefreshScope beans). 3) For Spring Cloud Bus, trigger '/actuator/bus-refresh' to refresh all instances. 4) Check if the config file name matches the application name and profile. 5) Verify Git credentials are correct and the repo is accessible. 6) Enable config server debug: 'logging.level.org.springframework.cloud.config=DEBUG'. 7) For Kubernetes, consider using ConfigMaps instead of Config Server.",
        "difficulty": "Medium"
    },
    {
        "question": "Eureka service registry shows services as 'DOWN' despite them being healthy and serving traffic. The health check endpoint returns 200 OK.",
        "answer": "1) Check the heartbeat interval - default is 30 seconds. If the service is slow to respond, Eureka marks it DOWN. 2) Configure 'eureka.instance.lease-renewal-interval-in-seconds=10' for faster heartbeats. 3) Verify the health check URL is correctly registered: 'eureka.instance.health-check-url-path=/actuator/health'. 4) Check if the service's hostname is resolvable from Eureka server. 5) Set 'eureka.instance.prefer-ip-address=true' if DNS is unreliable. 6) Increase 'eureka.server.eviction-interval-timer-in-ms' to avoid premature eviction. 7) Check network connectivity between service and Eureka server.",
        "difficulty": "Hard"
    },
    {
        "question": "Spring Boot application using @FeignClient to call another microservice gets 'Load balancer does not contain an instance for the service SERVICE-NAME'.",
        "answer": "1) Verify the service is registered in the service registry (Eureka/Consul). 2) Check the service name in @FeignClient matches the registered name exactly (case-sensitive). 3) Ensure spring-cloud-starter-loadbalancer is in dependencies (replaced Ribbon). 4) Check if the service registered with a different name or metadata. 5) Use 'spring.cloud.loadbalancer.ribbon.enabled=false' to ensure using Spring Cloud LoadBalancer. 6) Verify network connectivity between the caller and service registry. 7) Check the service's Eureka registration logs for the actual registered name.",
        "difficulty": "Medium"
    },
    {
        "question": "Distributed transaction across two Spring Boot microservices results in inconsistent data - Service A commits but Service B fails. No distributed transaction manager is configured.",
        "answer": "1) Implement the Saga pattern - compensate for Service A's changes when Service B fails. 2) Use event-driven architecture with Kafka/RabbitMQ for eventual consistency. 3) Implement outbox pattern: write to an outbox table in the same transaction, then a separate process publishes the event. 4) Use Spring Cloud Stream for reliable event publishing. 5) Implement idempotent operations in Service B to handle retries safely. 6) Add a reconciliation job that periodically checks and fixes inconsistencies. 7) Consider using Axon Framework or Camunda for saga orchestration.",
        "difficulty": "Hard"
    },
    {
        "question": "Spring Boot microservice with Kafka consumer processes messages out of order. The producer sends messages in sequence but the consumer receives them shuffled.",
        "answer": "1) Kafka only guarantees order within a partition - messages with different keys go to different partitions. 2) Use the same partition key for messages that must be ordered: 'producer.send(new ProducerRecord<>(topic, key, value))'. 3) Set 'max.poll.records=1' to process one message at a time (reduces throughput). 4) Use a single partition for the topic if ordering is critical (sacrifices parallelism). 5) Implement sequence numbers in messages and reorder in the consumer. 6) Use Kafka Streams for stateful processing with guaranteed ordering. 7) Configure 'enable.auto.commit=false' and commit offsets manually after processing.",
        "difficulty": "Hard"
    },
]

# ====== CATEGORY 6: Performance & Memory Issues ======
performance_scenarios = [
    {
        "question": "Spring Boot application's memory usage grows continuously over time until it crashes with OutOfMemoryError. Heap dumps show thousands of String objects.",
        "answer": "1) Use 'jmap -histo:live <pid>' or Eclipse MAT to analyze the heap dump. 2) Check for unbounded caches - use Caffeine or Guava cache with max size and eviction. 3) Look for memory leaks in static collections that grow indefinitely. 4) Check if log levels are set to DEBUG in production - logging creates many String objects. 5) Verify connection pools are properly bounded. 6) Use '-XX:+HeapDumpOnOutOfMemoryError -XX:HeapDumpPath=/path/to/dumps' for automatic heap dumps. 7) Profile with VisualVM or YourKit during load testing. 8) Check for ThreadLocal leaks - always call ThreadLocal.remove().",
        "difficulty": "Hard"
    },
    {
        "question": "API response time degrades from 200ms to 5+ seconds under load of 100 concurrent users. CPU usage is at 40%, memory is fine. What's the bottleneck?",
        "answer": "1) Check thread pool exhaustion - Tomcat default is 200 threads. Monitor with Actuator's /actuator/metrics/tomcat.threads. 2) Profile with async-profiler or YourKit to find hot methods. 3) Check database query performance - slow queries under concurrent load. 4) Look for synchronized blocks causing thread contention. 5) Check if external service calls are the bottleneck - add timeouts and circuit breakers. 6) Enable request tracing with Spring Cloud Sleuth/Micrometer Tracing. 7) Use 'jstack <pid>' to analyze thread states during the slowdown. 8) Consider async processing with @Async or reactive stack.",
        "difficulty": "Hard"
    },
    {
        "question": "Spring Boot application with WebClient makes 1000 concurrent HTTP calls and gets 'io.netty.channel.AbstractChannel$AnnotatedConnectException: Connection refused'.",
        "answer": "1) The OS has a limit on concurrent connections (ephemeral ports). On Linux, check '/proc/sys/net/ipv4/ip_local_port_range'. 2) Configure connection pooling in WebClient: 'HttpClient.create().connectionProvider(ConnectionProvider.builder('pool').maxConnections(500).build())'. 3) Set appropriate timeouts: '.timeout(Duration.ofSeconds(5))'. 4) Implement retry with backoff: '.retryWhen(Retry.backoff(3, Duration.ofMillis(100)))'. 5) Check if the target server has a connection limit. 6) Use 'tcp_tw_reuse=1' on Linux to reuse TIME_WAIT sockets. 7) Consider batching requests or using a message queue instead of direct HTTP calls.",
        "difficulty": "Hard"
    },
    {
        "question": "Spring Boot app's GC pauses are 2+ seconds causing request timeouts. The heap is 4GB and G1GC is being used.",
        "answer": "1) Reduce heap size if possible - 4GB may be too large for G1GC's default region size. 2) Tune G1GC: '-XX:MaxGCPauseMillis=200 -XX:G1HeapRegionSize=16m'. 3) Check for large object allocations that trigger mixed GC. 4) Use '-XX:+UnlockDiagnosticVMOptions -XX:+G1SummarizeRSetStats -XX:G1SummarizeRSetStatsPeriod=1' for GC analysis. 5) Consider ZGC or Shenandoah for sub-millisecond pauses: '-XX:+UseZGC'. 6) Profile object allocation rate with async-profiler. 7) Check if large responses are being loaded into memory - use streaming instead. 8) Enable GC logging: '-Xlog:gc*:file=gc.log:time,uptime:filecount=5,filesize=10m'.",
        "difficulty": "Hard"
    },
    {
        "question": "Spring Boot application with @Scheduled tasks starts executing tasks multiple times simultaneously after scaling to 3 instances. Each task should run once across all instances.",
        "answer": "1) @Scheduled runs on every instance by default - each JVM has its own scheduler. 2) Use ShedLock library: add 'net.javacrumbs.shedlock:shedlock-spring' and annotate with '@SchedulerLock(name = 'taskName', lockAtMostFor = '10m')'. 3) Configure ShedLock with a shared store (database, Redis, ZooKeeper). 4) For database: use 'shedlock-provider-jdbc-template' with a shared database. 5) For Redis: use 'shedlock-provider-redis-spring'. 6) Alternatively, use a distributed scheduler like Quartz with JDBC job store. 7) Or run scheduled tasks in a separate single-instance service.",
        "difficulty": "Medium"
    },
    {
        "question": "Spring Boot REST API returns responses slowly despite fast database queries. Profiling shows most time is spent in JSON serialization.",
        "answer": "1) Check for N+1 serialization - entities with lazy-loaded collections being serialized trigger additional queries. 2) Use DTOs instead of entities in REST responses. 3) Use @JsonIgnore on fields that don't need serialization. 4) Enable Jackson's afterburner module for faster serialization: 'jackson-module-afterburner'. 5) For large collections, use streaming JSON with Jackson's JsonGenerator. 6) Implement pagination to reduce response size. 7) Use response compression: 'server.compression.enabled=true'. 8) Consider using a faster JSON library like jsoniter or DSL-JSON for critical paths.",
        "difficulty": "Medium"
    },
]

# ====== CATEGORY 7: Configuration & Properties Issues ======
config_scenarios = [
    {
        "question": "Spring Boot application ignores environment variables for configuration. Setting 'SPRING_DATASOURCE_URL' has no effect - the application.properties value is used instead.",
        "answer": "1) Spring Boot property binding uses relaxed binding - 'SPRING_DATASOURCE_URL' should map to 'spring.datasource.url'. 2) Check the property source order - environment variables have higher precedence than application.properties. 3) Verify the environment variable is actually set: 'echo $SPRING_DATASOURCE_URL'. 4) For Docker/Kubernetes, check if the env var is properly injected into the container. 5) Use 'spring.config.import' for external configuration. 6) Enable property source logging: 'logging.level.org.springframework.core.env=DEBUG'. 7) Check if there's a @PropertySource overriding the environment variable.",
        "difficulty": "Medium"
    },
    {
        "question": "@ConfigurationProperties class is not binding values from application.yml. All fields are null despite the properties existing in the config file.",
        "answer": "1) Ensure the class has @ConfigurationProperties(prefix = 'my.prefix') AND @Component (or @EnableConfigurationProperties in a config class). 2) Check that the prefix matches exactly - case matters in YAML. 3) Verify YAML indentation is correct - wrong indentation creates nested objects instead of flat properties. 4) Add 'spring-boot-configuration-processor' dependency for metadata generation. 5) Check for getters/setters - binding requires them (or use record in Java 16+). 6) Use constructor binding with @ConstructorBinding for immutable classes. 7) Enable binding validation with @Validated on the class.",
        "difficulty": "Medium"
    },
    {
        "question": "Spring Boot profile-specific configuration (application-dev.yml) is not being loaded despite setting 'spring.profiles.active=dev' in application.yml.",
        "answer": "1) Check if '--spring.profiles.active=dev' command-line argument overrides the property file setting. 2) Verify the file is named correctly: 'application-dev.yml' (not 'application-development.yml'). 3) Check the file is in the classpath (src/main/resources). 4) For external configs, verify the search path includes the profile file. 5) Use 'spring.profiles.include' vs 'spring.profiles.active' - 'include' adds to active profiles, 'active' replaces. 6) Enable debug: 'spring.main.log-startup-info=true' to see which profiles are active. 7) Check if a higher-priority source (env var, command line) is overriding the profile.",
        "difficulty": "Easy"
    },
    {
        "question": "Spring Boot application reads secrets (DB password, API keys) from application.properties committed to Git. How do you externalize secrets securely?",
        "answer": "1) Use environment variables or Kubernetes Secrets for sensitive values. 2) Use Spring Cloud Vault or HashiCorp Vault for secret management. 3) Use AWS Secrets Manager or Azure Key Vault with Spring Cloud integrations. 4) Use 'spring.config.import' to load from external secret stores. 5) For local development, use .env files with dotenv library (never commit). 6) Use Jasypt for encrypted properties: '{cipher}encrypted-value'. 7) Remove committed secrets immediately - rotate them as they're now exposed. 8) Use git-secrets or pre-commit hooks to prevent future secret commits.",
        "difficulty": "Medium"
    },
    {
        "question": "Spring Boot application fails to start with 'IllegalArgumentException: Could not resolve placeholder X in string value Y'. The property is defined in a YAML file but uses a colon in the value.",
        "answer": "1) YAML values with colons need quoting: 'my.url: \"http://example.com:8080\"'. 2) For complex values, use the folded scalar: 'my.value: >' followed by the value on next line. 3) Check if the colon is being interpreted as a YAML key-value separator. 4) Use double quotes around the entire value to escape special characters. 5) For URLs, consider using 'spring.boot.admin.client.url' format. 6) Test the YAML parsing in isolation with a YAML parser. 7) Use properties file format instead of YAML for problematic values.",
        "difficulty": "Easy"
    },
]

# ====== CATEGORY 8: Testing Issues ======
testing_scenarios = [
    {
        "question": "@SpringBootTest test fails with 'IllegalStateException: Failed to load ApplicationContext'. The application runs fine outside tests. The error points to a missing bean.",
        "answer": "1) Tests use a different classpath - check if test dependencies are missing. 2) Use @MockBean to mock external dependencies that aren't available in tests. 3) Check if @ComponentScan is excluding test packages. 4) Use @TestPropertySource to provide test-specific properties. 5) For missing external services, use Testcontainers or WireMock. 6) Check if a @ConditionalOnProperty is excluding a required bean in test profile. 7) Use @DataJpaTest, @WebMvcTest slice tests instead of full @SpringBootTest for faster, more focused tests. 8) Enable debug logging in tests: '@SpringBootTest(properties = \"logging.level.org.springframework=DEBUG\")'.",
        "difficulty": "Medium"
    },
    {
        "question": "Integration test with @DataJpaTest fails with 'TransactionRequiredException' when testing a @Modifying repository method.",
        "answer": "1) @DataJpaTest runs each test method in a transaction that rolls back - but @Modifying methods need explicit transaction management. 2) Add @Transactional to the test method. 3) For @Modifying queries, use '@Modifying @Transactional' on the repository method. 4) Use '@DataJpaTest(showSql = true)' to see the generated SQL. 5) Check if the test database schema is properly initialized - use @Sql to load test data. 6) For H2 in-memory database, verify the dialect is correct: 'spring.jpa.database-platform=org.hibernate.dialect.H2Dialect'. 7) Use Testcontainers with a real database for more accurate integration tests.",
        "difficulty": "Medium"
    },
    {
        "question": "MockMvc test for a REST endpoint returns 401 Unauthorized despite using @WithMockUser. The security configuration should allow authenticated access.",
        "answer": "1) Ensure 'spring-security-test' dependency is included. 2) @WithMockUser requires 'spring-security-test' on the classpath. 3) For @WebMvcTest, add '@AutoConfigureMockMvc' and import the security config. 4) Check if the SecurityFilterChain is being loaded in the test context. 5) Use 'mockMvc.perform(get('/endpoint').with(SecurityMockMvcRequestPostProcessors.user('testUser')))' as an alternative. 6) Verify the mock user has the required role: '@WithMockUser(username = 'admin', roles = {'ADMIN'})'. 7) For Spring Security 6, ensure the test uses the correct security context setup.",
        "difficulty": "Hard"
    },
    {
        "question": "Test with Testcontainers PostgreSQL fails on CI/CD pipeline with 'Could not find a valid Docker environment'. Tests pass locally.",
        "answer": "1) CI/CD runner doesn't have Docker-in-Docker configured. 2) For GitHub Actions, use 'services' in the workflow to run PostgreSQL container. 3) Or use 'docker/setup-buildx-action' and ensure Docker socket is mounted. 4) Alternative: use embedded databases for CI (H2) and Testcontainers for local testing. 5) Configure Testcontainers to use a Docker host: 'testcontainers.reuse.enable=true'. 6) For GitLab CI, add 'docker:dind' service. 7) Use 'ryuk' container cleanup: 'testcontainers.ryuk.disabled=false'. 8) Consider using @TestPropertySource to switch to H2 for CI: 'spring.datasource.url=jdbc:h2:mem:testdb'.",
        "difficulty": "Hard"
    },
]

# ====== CATEGORY 9: Logging & Monitoring Issues ======
logging_scenarios = [
    {
        "question": "Spring Boot application logs are not appearing in the expected file. The logback-spring.xml is configured but only console output works.",
        "answer": "1) Verify logback-spring.xml is in src/main/resources (classpath root). 2) Check the file appender configuration - ensure the directory exists and is writable. 3) Use 'logging.file.name=app.log' or 'logging.file.path=/var/log/myapp' in application.properties. 4) Check file permissions - the process user must have write access. 5) Verify no other logging configuration is overriding (logback.xml takes precedence over logback-spring.xml). 6) Enable logback debug: '-Dlogback.debug=true' to see configuration loading. 7) Check if log rotation is deleting logs immediately - review rolling policy settings.",
        "difficulty": "Easy"
    },
    {
        "question": "Spring Boot Actuator's /actuator/metrics endpoint returns empty data despite having micrometer-registry-prometheus dependency.",
        "answer": "1) Verify the endpoint is exposed: 'management.endpoints.web.exposure.include=metrics,prometheus'. 2) Check 'management.endpoint.metrics.enabled=true'. 3) For Prometheus, use '/actuator/prometheus' endpoint instead of '/actuator/metrics'. 4) Verify micrometer-registry-prometheus is actually on the classpath: 'mvn dependency:tree | grep micrometer'. 5) Check if custom MeterRegistry configuration is overriding the auto-configured one. 6) Ensure metrics are being recorded - add a counter or timer and verify it increments. 7) Use '/actuator/metrics/{metricName}' to query specific metrics.",
        "difficulty": "Medium"
    },
    {
        "question": "Distributed tracing with Micrometer Tracing and Zipkin shows incomplete traces - some service calls are missing from the trace timeline.",
        "answer": "1) Check if all services have the tracing dependencies (micrometer-tracing-bridge-brave or micrometer-tracing-bridge-otel). 2) Verify the propagation format matches across services (W3C vs B3). 3) Check if async calls (@Async, CompletableFuture) are propagating the trace context - use TaskDecorator. 4) For WebClient/RestTemplate calls, ensure the tracing filter is applied. 5) Check Zipkin reporter configuration - 'management.zipkin.tracing.endpoint'. 6) Verify sampling rate isn't too low: 'management.tracing.sampling.probability=1.0' for all traces. 7) Check if trace context is lost across thread boundaries - use Sleuth's async support.",
        "difficulty": "Hard"
    },
    {
        "question": "Spring Boot application's log output contains sensitive data (passwords, tokens) in plain text. The team needs to sanitize logs without losing debugging capability.",
        "answer": "1) Use Logback's masking filter - create a custom ClassicConverter that redacts sensitive patterns. 2) Use 'logback-spring.xml' with a regex filter: '<regexFilter>.*password.*</regexFilter>'. 3) For JSON logging (logstash-logback-encoder), use a JsonGeneratorDecorator to mask fields. 4) Use @JsonInclude(JsonInclude.Include.NON_NULL) on DTOs to avoid logging null/sensitive fields. 5) Configure 'logging.pattern.console' to exclude sensitive patterns. 6) Use Spring Boot's 'logging.pattern.dateformat' for consistent formatting. 7) Implement a custom Appender that filters sensitive data before writing. 8) Use structured logging with MDC for traceable but sanitized logs.",
        "difficulty": "Medium"
    },
]

# ====== CATEGORY 10: Deployment & Production Issues ======
deployment_scenarios = [
    {
        "question": "Spring Boot fat JAR works locally but fails in production with 'no main manifest attribute'. The JAR was built with 'mvn package'.",
        "answer": "1) Use 'mvn clean package spring-boot:repackage' or ensure spring-boot-maven-plugin is configured with 'repackage' goal. 2) Check pom.xml has: '<plugin><groupId>org.springframework.boot</groupId><artifactId>spring-boot-maven-plugin</artifactId></plugin>'. 3) For Gradle: use './gradlew bootJar' instead of './gradlew jar'. 4) Verify the Main-Class in MANIFEST.MF points to your @SpringBootApplication class. 5) Check if the packaging is set to 'jar' in pom.xml. 6) For multi-module projects, ensure the plugin is in the correct module's pom.xml. 7) Run 'jar tf target/app.jar | grep MANIFEST' to verify the manifest.",
        "difficulty": "Easy"
    },
    {
        "question": "Spring Boot application deployed as a WAR to Tomcat returns 404 for all endpoints. The same application works as a JAR with embedded Tomcat.",
        "answer": "1) Extend SpringBootServletInitializer and override the configure method. 2) Set packaging to 'war' in pom.xml. 3) Mark embedded Tomcat as provided: '<scope>provided</scope>' for spring-boot-starter-tomcat. 4) Ensure the servlet context path matches - Tomcat may deploy under '/app-name'. 5) Check Tomcat's manager console for deployment errors. 6) Verify the WAR contains WEB-INF/classes and WEB-INF/lib directories. 7) Check Tomcat version compatibility with Spring Boot version. 8) Review Tomcat's catalina.out logs for deployment errors.",
        "difficulty": "Medium"
    },
    {
        "question": "Kubernetes liveness probe kills the Spring Boot pod repeatedly. The application is healthy but the probe fails after 30 seconds.",
        "answer": "1) Increase initialDelaySeconds - Spring Boot startup may take longer than the probe timeout. 2) Configure 'livenessProbe: { httpGet: { path: /actuator/health/liveness, port: 8080 }, initialDelaySeconds: 60, periodSeconds: 10, failureThreshold: 3 }'. 3) Use readiness probe separately: 'readinessProbe: { httpGet: { path: /actuator/health/readiness, port: 8080 } }'. 4) Enable Spring Boot's liveness/readiness state: 'management.health.probes.enabled=true'. 5) Check if the application is stuck during startup (database migration, bean initialization). 6) Increase timeoutSeconds if the health check itself is slow. 7) Review application logs for startup bottlenecks.",
        "difficulty": "Medium"
    },
    {
        "question": "Spring Boot application in Docker container can't connect to a database running on the host machine using 'localhost' as the hostname.",
        "answer": "1) Inside Docker, 'localhost' refers to the container, not the host. Use 'host.docker.internal' (Docker Desktop) or the host's IP address. 2) For Linux Docker, use '--network=host' or the bridge network gateway IP. 3) Get the gateway IP: 'docker network inspect bridge | grep Gateway'. 4) For Docker Compose, put both containers on the same network and use the service name. 5) For Kubernetes, use the service DNS name or external IP. 6) Configure the datasource URL accordingly: 'jdbc:postgresql://host.docker.internal:5432/mydb'. 7) For production, never use localhost - always use proper service discovery or DNS.",
        "difficulty": "Easy"
    },
    {
        "question": "After deploying a new Spring Boot version, users report seeing stale content. The application uses static resources (CSS, JS) that aren't updating.",
        "answer": "1) Add resource versioning: 'spring.web.resources.chain.strategy.content.enabled=true'. 2) Set cache control headers: 'spring.web.resources.cache.period=0' for development. 3) Use content-based hashing for static resources: 'spring.web.resources.chain.strategy.content.paths=/**'. 4) For CDN deployments, invalidate the cache after deployment. 5) Add version query parameters: 'app.js?v=1.2.3'. 6) Configure proper Cache-Control headers: 'spring.web.resources.cache.cachecontrol.max-age=31536000' with versioned URLs. 7) Use build tools to append content hashes to filenames during build.",
        "difficulty": "Medium"
    },
]

# ====== CATEGORY 11: Exception Handling & Error Scenarios ======
exception_scenarios = [
    {
        "question": "Spring Boot application throws 'StackOverflowError' in production but not in testing. The stack trace shows recursive calls in a JPA entity's toString() method.",
        "answer": "1) Bidirectional JPA relationships cause infinite recursion in toString(), equals(), hashCode(). 2) Use @ToString.Exclude (Lombok) or manually exclude the back-reference in toString(). 3) For equals/hashCode, use only the entity ID or a business key - never use the relationship side. 4) Use @EqualsAndHashCode.Exclude on the back-reference field. 5) If not using Lombok, override toString() to exclude the circular reference. 6) Use DTOs for API responses instead of entities to avoid serialization issues. 7) Add logging to catch the recursion early: log the entity ID before toString() calls.",
        "difficulty": "Medium"
    },
    {
        "question": "Spring Boot application throws 'ConcurrentModificationException' when iterating over a list that's being modified by another thread. The list is a @Component-scoped bean.",
        "answer": "1) Spring beans are singletons by default - a list in a singleton bean is shared across all threads. 2) Use 'Collections.synchronizedList(new ArrayList<>())' or 'CopyOnWriteArrayList'. 3) Better: don't store mutable state in singleton beans - use a proper data store. 4) If caching is needed, use Spring Cache with @Cacheable and a thread-safe cache implementation. 5) Use ConcurrentHashMap instead of HashMap for concurrent access. 6) For request-scoped data, use '@Scope('request')' or ThreadLocal. 7) Review the design - shared mutable state in Spring beans is an anti-pattern.",
        "difficulty": "Medium"
    },
    {
        "question": "Application throws 'NullPointerException' in a @Service method. The injected @Repository dependency is null despite having @Autowired annotation.",
        "answer": "1) The service class might be instantiated with 'new' instead of being managed by Spring. 2) Check if the class has @Service or @Component annotation. 3) Verify the package is included in component scanning. 4) Check for circular dependencies causing partial initialization. 5) Use constructor injection instead of field injection - it fails fast if dependencies can't be injected. 6) Check if the repository is excluded by any @ComponentScan filter. 7) For test classes, ensure @ExtendWith(SpringExtension.class) or @SpringBootTest is used.",
        "difficulty": "Easy"
    },
    {
        "question": "Spring Boot application throws 'BeanCurrentlyInCreationException' during startup. The error mentions a bean that uses @PostConstruct to initialize resources.",
        "answer": "1) The @PostConstruct method is triggering access to another bean that depends on the current bean - creating a cycle. 2) Use @Lazy on one of the dependencies to break the cycle. 3) Move the initialization logic to a separate bean that doesn't participate in the cycle. 4) Use ApplicationListener<ContextRefreshedEvent> instead of @PostConstruct for post-startup initialization. 5) Implement SmartInitializingSingleton for post-processing after all beans are created. 6) Use @DependsOn to control bean creation order. 7) Refactor to eliminate the circular dependency - it's a design smell.",
        "difficulty": "Hard"
    },
    {
        "question": "Spring Boot throws 'MethodNotAllowedException' or 'HttpRequestMethodNotSupportedException' for a valid POST request. The controller has @PostMapping configured.",
        "answer": "1) Check if Spring Security is blocking the method - CSRF protection rejects POST without a valid token. 2) Verify the URL path matches exactly - trailing slashes matter. 3) Check if a filter is intercepting and consuming the request before it reaches the controller. 4) For @RestController, ensure it's not confused with @Controller + @ResponseBody. 5) Check if there's a conflicting mapping at the class level. 6) Verify the HTTP method in the client request - some proxies convert POST to GET. 7) Enable 'logging.level.org.springframework.web=DEBUG' to trace the request mapping.",
        "difficulty": "Medium"
    },
]

# ====== CATEGORY 12: Transaction Management Issues ======
transaction_scenarios = [
    {
        "question": "@Transactional method in Spring Boot doesn't roll back when an exception is thrown. The database changes are committed despite the error.",
        "answer": "1) By default, @Transactional only rolls back on RuntimeException and Error - not checked exceptions. 2) Use '@Transactional(rollbackFor = Exception.class)' to roll back on all exceptions. 3) Check if the exception is being caught inside the method - caught exceptions don't trigger rollback. 4) Verify the method is public - @Transactional on private/protected methods is ignored. 5) Ensure the method is called from outside the class - self-invocation bypasses the proxy. 6) Check if the transaction manager is properly configured. 7) For programmatic rollback, use 'TransactionAspectSupport.currentTransactionStatus().setRollbackOnly()'.",
        "difficulty": "Medium"
    },
    {
        "question": "Spring Boot application with @Transactional and @Async on the same method throws 'TransactionRequiredException'. The transaction context is lost.",
        "answer": "1) @Async runs in a separate thread - the transaction context doesn't propagate across threads by default. 2) Remove @Transactional from the async method - manage transactions within the async method instead. 3) Use a TransactionTemplate for programmatic transaction management inside the async method. 4) Create a separate service method with @Transactional and call it from the @Async method. 5) Configure a TaskDecorator to propagate transaction context (complex and not recommended). 6) Better pattern: @Async method collects work, then calls a @Transactional method to persist results. 7) Use @TransactionalEventListener for transaction-bound async events.",
        "difficulty": "Hard"
    },
    {
        "question": "Two @Transactional methods calling each other within the same class - the inner method's propagation setting (REQUIRES_NEW) is ignored. Both run in the same transaction.",
        "answer": "1) Spring's AOP proxy doesn't work for self-invocation - calling method B from method A in the same class bypasses the proxy. 2) Inject the service into itself (self-injection) to go through the proxy. 3) Use AopContext.currentProxy() to get the proxied reference: '((MyService) AopContext.currentProxy()).methodB()'. 4) Enable proxy exposure: '@EnableAspectJAutoProxy(exposeProxy = true)'. 5) Better: split the methods into separate service classes. 6) Use TransactionTemplate for programmatic transaction control. 7) This is a common Spring gotcha - always be aware of proxy limitations.",
        "difficulty": "Hard"
    },
    {
        "question": "Spring Boot batch processing with @Transactional processes 100K records and runs out of memory. The transaction holds all entities in the persistence context.",
        "answer": "1) Hibernate's first-level cache grows with every entity in the transaction. 2) Use chunk processing: process 1000 records per transaction with 'entityManager.flush()' and 'entityManager.clear()' after each chunk. 3) Use Spring Batch with chunk-oriented processing: '<chunk reader='...' processor='...' writer='...' commit-interval='1000'/>'. 4) Set 'spring.jpa.properties.hibernate.jdbc.batch_size=1000' for JDBC batching. 5) Use 'StatelessSession' for bulk operations - it doesn't maintain a persistence context. 6) Use native SQL for bulk inserts/updates instead of JPA. 7) Consider 'JdbcTemplate.batchUpdate()' for better performance.",
        "difficulty": "Hard"
    },
]

# ====== CATEGORY 13: Cache Issues ======
cache_scenarios = [
    {
        "question": "Spring Boot @Cacheable method returns stale data after the underlying database record is updated. The cache isn't being invalidated.",
        "answer": "1) Use @CacheEvict on the update method: '@CacheEvict(value = 'myCache', key = '#id')'. 2) Use @CachePut on the update method to update the cache with the new value. 3) Set a TTL on the cache: configure Caffeine with 'expireAfterWrite=10m'. 4) For Redis cache, use 'spring.cache.redis.time-to-live=600000'. 5) Use 'cacheManager.getCache('myCache').clear()' for programmatic eviction. 6) Check if the cache key generation is consistent between @Cacheable and @CacheEvict. 7) Consider using 'unless' condition on @Cacheable to skip caching for certain results.",
        "difficulty": "Medium"
    },
    {
        "question": "Spring Boot with Redis cache throws 'RedisConnectionFailureException' intermittently. The Redis server is running and accessible from the application server.",
        "answer": "1) Check Redis connection pool settings - default Lettuce pool may be exhausted. 2) Configure connection pooling: 'spring.data.redis.lettuce.pool.max-active=20'. 3) Set connection timeout: 'spring.data.redis.timeout=5000'. 4) Check if Redis is hitting max client connections: 'CONFIG GET maxclients'. 5) Enable Lettuce auto-reconnect - it should reconnect automatically but verify the version. 6) For high availability, use Redis Sentinel or Redis Cluster configuration. 7) Monitor Redis memory usage - OOM causes connection drops. 8) Add circuit breaker for Redis operations to degrade gracefully.",
        "difficulty": "Hard"
    },
    {
        "question": "Spring Boot @Cacheable with Caffeine cache shows 0% hit rate despite being called repeatedly with the same parameters.",
        "answer": "1) Check if the cache key is being generated correctly - different parameter instances create different keys. 2) For custom objects as keys, ensure equals() and hashCode() are properly implemented. 3) Verify the cache is actually enabled: '@EnableCaching' on a configuration class. 4) Check cache size - if max size is too small, entries are evicted before being hit. 5) Use 'spring.cache.cache-names=myCache' to pre-configure the cache. 6) Enable cache statistics: configure Caffeine with 'recordStats()' and check via CacheManager. 7) Check if @Cacheable condition ('unless' or 'condition') is preventing caching.",
        "difficulty": "Medium"
    },
]

# ====== CATEGORY 14: Async & Reactive Issues ======
async_scenarios = [
    {
        "question": "Spring Boot @Async method executes synchronously despite having @Async annotation. The calling thread waits for the async method to complete.",
        "answer": "1) @EnableAsync is missing on a configuration class. 2) The async method is called from within the same class - self-invocation bypasses the proxy. 3) The method is private or final - Spring can't proxy it. 4) The return type isn't CompletableFuture or void - async requires these. 5) Check if a custom AsyncConfigurer is overriding the executor. 6) Verify the thread pool isn't exhausted - configure 'spring.task.execution.pool.core-size'. 7) Enable async debug logging: 'logging.level.org.springframework.aop=DEBUG'.",
        "difficulty": "Medium"
    },
    {
        "question": "Spring Boot application with @Async methods throws 'TaskRejectedException: Executor did not accept task' under load. The thread pool is configured with core-size=5.",
        "answer": "1) The thread pool queue is full - default queue capacity is Integer.MAX_VALUE but custom executors may have limits. 2) Increase pool size: 'spring.task.execution.pool.max-size=20'. 3) Configure queue capacity: 'spring.task.execution.pool.queue-capacity=100'. 4) Set a rejection policy: use CallerRunsPolicy to execute in the calling thread when pool is full. 5) Monitor thread pool metrics with Actuator. 6) Consider using a message queue (Kafka/RabbitMQ) for high-volume async processing. 7) Implement backpressure - reject requests gracefully when the system is overloaded.",
        "difficulty": "Hard"
    },
    {
        "question": "Spring WebFlux application with reactive streams shows 'BackpressureException: The receiver is overrun by more signals than expected'. The producer is faster than the consumer.",
        "answer": "1) Implement proper backpressure handling - use 'onBackpressureBuffer()', 'onBackpressureDrop()', or 'onBackpressureLatest()'. 2) Use 'limitRate()' to request a bounded number of elements. 3) For database operations, use R2DBC instead of blocking JPA in reactive pipelines. 4) Configure the producer to respect demand: use 'Flux.create()' with OverflowStrategy. 5) Use 'bufferTimeout()' to batch elements before processing. 6) Monitor reactor metrics: 'reactor.core.publisher.Metrics' for backpressure events. 7) Consider using 'publishOn()' and 'subscribeOn()' with appropriate schedulers to balance load.",
        "difficulty": "Hard"
    },
]

# ====== CATEGORY 15: Build & Dependency Issues ======
build_scenarios = [
    {
        "question": "Maven build fails with 'Dependency convergence error' for Spring Boot project. Two transitive dependencies require different versions of the same library.",
        "answer": "1) Run 'mvn dependency:tree' to identify the conflicting dependencies. 2) Use <dependencyManagement> in pom.xml to enforce a single version. 3) Use <exclusions> to remove the unwanted transitive dependency. 4) Use Spring Boot's BOM: '<dependencyManagement><dependencies><dependency><groupId>org.springframework.boot</groupId><artifactId>spring-boot-dependencies</artifactId><version>3.2.0</version><type>pom</type><scope>import</scope></dependency></dependencies></dependencyManagement>'. 5) Run 'mvn enforcer:enforce' with dependencyConvergence rule to catch issues early. 6) Use 'mvn dependency:analyze' to find unused declared dependencies. 7) Check for dependency conflicts with 'mvn dependency:tree -Dverbose'.",
        "difficulty": "Medium"
    },
    {
        "question": "Spring Boot application works with 'mvn spring-boot:run' but the packaged JAR fails with 'ClassNotFoundException' for a class that's clearly in the dependencies.",
        "answer": "1) The dependency scope might be 'provided' or 'test' - it's available during 'mvn spring-boot:run' but not packaged. 2) Check the dependency scope in pom.xml - change 'provided' to 'compile' if it needs to be in the JAR. 3) Run 'jar tf target/app.jar | grep <missing-class>' to verify it's in the JAR. 4) For spring-boot-maven-plugin, ensure the 'repackage' goal is executed. 5) Check if the class is in a nested JAR (BOOT-INF/lib/) - Spring Boot's classloader should handle this. 6) Verify the MANIFEST.MF has the correct Spring-Boot-Class-Path. 7) Use 'mvn clean package' to ensure a clean build.",
        "difficulty": "Medium"
    },
    {
        "question": "Gradle build for Spring Boot project fails with 'Could not resolve all dependencies for configuration :compileClasspath'. The dependencies resolve fine in other projects.",
        "answer": "1) Check if the repository configuration includes Maven Central: 'repositories { mavenCentral() }'. 2) Verify the dependency coordinates are correct - group, name, version. 3) Check for network/proxy issues - configure proxy in gradle.properties if behind a corporate firewall. 4) Run './gradlew dependencies --configuration compileClasspath' to see the resolution tree. 5) Clear Gradle cache: 'rm -rf ~/.gradle/caches/' and rebuild. 6) Check if a dependency is from a private repository that requires authentication. 7) Use './gradlew build --refresh-dependencies' to force re-download. 8) Verify the Gradle version is compatible with the Spring Boot plugin version.",
        "difficulty": "Easy"
    },
]

# ====== CATEGORY 16: Specific Spring Boot Component Issues ======
component_scenarios = [
    {
        "question": "Spring Boot @Scheduled task stops running after one execution. The cron expression is '0 0/5 * * * *' (every 5 minutes) but it only runs once.",
        "answer": "1) Check if the task method throws an exception - uncaught exceptions stop future executions. 2) Wrap the task body in try-catch and log exceptions. 3) Verify the cron expression is valid - use a cron expression validator. 4) Check if the scheduler thread pool is exhausted - configure 'spring.task.scheduling.pool.size'. 5) Use 'fixedDelay' or 'fixedRate' instead of cron for simpler scheduling. 6) Enable scheduling debug: 'logging.level.org.springframework.scheduling=DEBUG'. 7) Check if the application is in a state where the scheduler is paused (e.g., during shutdown).",
        "difficulty": "Medium"
    },
    {
        "question": "Spring Boot @EventListener method doesn't receive events published with ApplicationEventPublisher. The event class extends ApplicationEvent.",
        "answer": "1) The listener class must be a Spring bean (@Component) - otherwise it's not registered. 2) Check if the event publisher is the same ApplicationContext that the listener is registered in. 3) For async event listening, add @Async and @EnableAsync - but ensure the executor is configured. 4) Verify the event class matches exactly - generic type erasure can cause mismatches. 5) Use @TransactionalEventListener if you need the event to be processed after transaction commit. 6) Check if the event is being published before the listener is registered (during startup). 7) Enable event debug logging: 'logging.level.org.springframework.context.event=DEBUG'.",
        "difficulty": "Medium"
    },
    {
        "question": "Spring Boot CommandLineRunner executes but the application exits immediately after. The application should stay running to serve HTTP requests.",
        "answer": "1) Missing spring-boot-starter-web dependency - without it, there's no web server to keep the app running. 2) Check if 'spring.main.web-application-type' is set to 'none'. 3) Verify the main class has @SpringBootApplication (which includes @EnableAutoConfiguration). 4) Check if an exception in CommandLineRunner causes context closure. 5) For non-web apps that should stay running, use CountDownLatch or SpringApplication.run().wait(). 6) Check if System.exit() is being called somewhere. 7) Verify no other bean is calling ApplicationContext.close().",
        "difficulty": "Easy"
    },
    {
        "question": "Spring Boot @Retryable annotation doesn't retry the method on failure. The method throws RuntimeException but executes only once.",
        "answer": "1) @EnableRetry is missing on a configuration class. 2) spring-retry dependency is not on the classpath: add 'org.springframework.retry:spring-retry'. 3) The method is called from within the same class - self-invocation bypasses the proxy. 4) The exception type doesn't match 'include' or is in 'exclude' list. 5) Check maxAttempts and backoff settings - defaults are 3 attempts with 1 second delay. 6) Verify the method is public - @Retryable doesn't work on private methods. 7) Enable retry debug: 'logging.level.org.springframework.retry=DEBUG'.",
        "difficulty": "Medium"
    },
]

# ====== CATEGORY 17: API Gateway & Routing Issues ======
gateway_scenarios = [
    {
        "question": "Spring Cloud Gateway route forwards requests but the downstream service receives wrong headers. The Authorization header is missing in the forwarded request.",
        "answer": "1) Spring Cloud Gateway filters may be stripping sensitive headers. 2) Configure 'spring.cloud.gateway.default-filters' to preserve headers. 3) Check if a custom GlobalFilter is modifying the request. 4) For sensitive headers, add them explicitly in a filter: 'exchange.getRequest().mutate().header('Authorization', token)'. 5) Verify the route predicate isn't filtering out the header. 6) Check if CORS configuration is interfering with header forwarding. 7) Enable gateway debug logging: 'logging.level.org.springframework.cloud.gateway=DEBUG'.",
        "difficulty": "Hard"
    },
    {
        "question": "Spring Cloud Gateway returns 503 Service Unavailable for a route that's configured to forward to a service registered in Eureka. The service is UP in Eureka dashboard.",
        "answer": "1) Check the route configuration - 'lb://SERVICE-NAME' uses load balancer to find instances. 2) Verify the service name matches exactly (case-sensitive) with Eureka registration. 3) Check if Spring Cloud LoadBalancer is configured (replaced Ribbon in Spring Cloud 2020+). 4) Verify 'spring.cloud.gateway.discovery.locator.enabled=true' for auto-discovery routes. 5) Check if the service's health endpoint is returning UP. 6) Test the route with 'curl -v http://gateway:8080/route' to see the full error. 7) Check gateway logs for load balancer instance resolution failures.",
        "difficulty": "Hard"
    },
]

# ====== CATEGORY 18: Data Migration & Schema Issues ======
migration_scenarios = [
    {
        "question": "Flyway migration fails with 'Migration V2__add_column.sql failed: ERROR: column X already exists'. The migration script adds a column that may already exist from a manual DB change.",
        "answer": "1) Use 'flyway repair' to mark the migration as applied if the column already exists. 2) Make migrations idempotent: 'ALTER TABLE my_table ADD COLUMN IF NOT EXISTS new_column VARCHAR(255)' (PostgreSQL). 3) For MySQL: use 'ALTER TABLE my_table ADD COLUMN new_column VARCHAR(255)' with error handling. 4) Set 'spring.flyway.baseline-on-migrate=true' for existing databases. 5) Use 'spring.flyway.out-of-order=true' if migrations were applied out of sequence. 6) Create a baseline migration: 'flyway baseline' to mark the current schema state. 7) Never modify applied migration files - create new migrations for changes.",
        "difficulty": "Medium"
    },
    {
        "question": "Spring Boot with Hibernate auto-ddl (spring.jpa.hibernate.ddl-auto=update) creates duplicate indexes on startup, causing slow inserts.",
        "answer": "1) Never use 'ddl-auto=update' in production - use Flyway/Liquibase for schema management. 2) Set 'spring.jpa.hibernate.ddl-auto=validate' in production to check schema without modifying. 3) Check if @Index annotations are duplicated on the entity. 4) Verify the entity isn't being scanned by multiple EntityManagerFactories. 5) Use 'spring.jpa.generate-ddl=false' to disable DDL generation entirely. 6) Review the schema with 'SHOW INDEX FROM table_name' and remove duplicates manually. 7) Use database-specific tools to analyze and optimize indexes.",
        "difficulty": "Medium"
    },
    {
        "question": "Liquibase migration fails with 'Validation Failed: 1 checksums differ'. The migration file wasn't modified but the checksum changed.",
        "answer": "1) Line ending changes (CRLF vs LF) can change checksums even if content is the same. 2) Run 'liquibase clearChecksums' to recalculate all checksums. 3) For Spring Boot: 'spring.liquibase.clear-checksums=true' (one-time use). 4) Check if the changelog file was reformatted by an IDE or linter. 5) Use 'liquibase validate' to see which changesets have mismatched checksums. 6) For intentional changes, use 'liquibase calculateChecksum' to get the new checksum and update the database. 7) Store changelog files with consistent line endings in version control (use .gitattributes).",
        "difficulty": "Medium"
    },
]

# ====== CATEGORY 19: Internationalization & Localization Issues ======
i18n_scenarios = [
    {
        "question": "Spring Boot internationalization (i18n) returns English messages despite the client sending 'Accept-Language: fr-FR' header. French message properties file exists.",
        "answer": "1) Verify the message file naming: 'messages_fr.properties' or 'messages_fr_FR.properties'. 2) Check if MessageSource is properly configured with 'spring.messages.basename=messages'. 3) Verify the file encoding is UTF-8 - non-ASCII characters in properties files need native2ascii or use UTF-8 encoding. 4) For Spring Boot 2.6+, set 'spring.messages.encoding=UTF-8'. 5) Check if the LocaleResolver is configured correctly - AcceptHeaderLocaleResolver is default. 6) Verify the message key exists in the French properties file. 7) Enable i18n debug: 'logging.level.org.springframework.context.support=DEBUG'.",
        "difficulty": "Medium"
    },
]

# ====== CATEGORY 20: WebSocket & Real-time Issues ======
websocket_scenarios = [
    {
        "question": "Spring Boot WebSocket connection fails with 'WebSocket connection to ws://localhost:8080/ws failed: Error during WebSocket handshake: Unexpected response code: 200'.",
        "answer": "1) The WebSocket endpoint is being handled by a regular HTTP handler instead of the WebSocket handler. 2) Verify WebSocket configuration: implement WebSocketConfigurer and register handlers. 3) Check if Spring Security is blocking the WebSocket upgrade - add '.requestMatchers('/ws/**').permitAll()'. 4) For SockJS fallback, configure with '.withSockJS()'. 5) Verify the WebSocket dependency is included: 'spring-boot-starter-websocket'. 6) Check if a filter is consuming the request before WebSocket handler. 7) Enable WebSocket debug: 'logging.level.org.springframework.web.socket=DEBUG'.",
        "difficulty": "Medium"
    },
    {
        "question": "Spring Boot STOMP WebSocket with SimpMessagingTemplate fails to send messages to specific users. 'convertAndSendToUser' doesn't deliver messages.",
        "answer": "1) User principal must be set during WebSocket handshake - configure a HandshakeInterceptor or ChannelInterceptor. 2) For Spring Security, ensure the WebSocket connection is authenticated. 3) The destination prefix for user-specific messages is '/user/' - verify the client subscribes to '/user/queue/messages'. 4) Check if the user registry is properly configured - use 'SimpUserRegistry' to verify connected users. 5) For clustered deployments, use a message broker (RabbitMQ/ActiveMQ) instead of SimpleBroker. 6) Verify the session ID is consistent across the WebSocket connection. 7) Enable STOMP debug: 'logging.level.org.springframework.messaging=DEBUG'.",
        "difficulty": "Hard"
    },
]

# ====== CATEGORY 21: Email & External Service Integration ======
email_scenarios = [
    {
        "question": "Spring Boot email service using JavaMailSender throws 'MailSendException: Could not connect to SMTP host: smtp.gmail.com, port: 587'. The SMTP credentials are correct.",
        "answer": "1) Check network connectivity: 'telnet smtp.gmail.com 587' from the application server. 2) For Gmail, enable 'Less secure app access' or use App Passwords with 2FA. 3) Configure TLS properly: 'spring.mail.properties.mail.smtp.starttls.enable=true'. 4) Set authentication: 'spring.mail.properties.mail.smtp.auth=true'. 5) Check if a firewall is blocking outbound SMTP connections. 6) For AWS/GCP, SMTP ports may be blocked by default - request port 587 access. 7) Use 'spring.mail.test-connection=true' to verify configuration on startup. 8) Consider using a transactional email service (SendGrid, SES) instead of direct SMTP.",
        "difficulty": "Medium"
    },
]

# ====== CATEGORY 22: File Handling & I/O Issues ======
file_scenarios = [
    {
        "question": "Spring Boot file upload works locally but fails in production with 'java.io.FileNotFoundException: /tmp/upload_XXX.tmp (No space left on device)'.",
        "answer": "1) The /tmp partition is full - clean up old files: 'find /tmp -name 'upload_*' -mtime +1 -delete'. 2) Configure a different temp directory: '-Djava.io.tmpdir=/var/app/tmp'. 3) Set 'spring.servlet.multipart.location=/var/app/tmp' for multipart uploads. 4) Monitor disk usage with 'df -h' and set up alerts. 5) Implement cleanup of temporary files after processing. 6) For containerized apps, ensure the container has sufficient disk space. 7) Use streaming upload instead of storing files in temp: use InputStream directly.",
        "difficulty": "Medium"
    },
    {
        "question": "Spring Boot application serving static files returns 304 Not Modified for files that have been updated. Clients see stale content.",
        "answer": "1) Spring Boot's resource handler uses ETag and Last-Modified headers for caching. 2) Disable caching for development: 'spring.web.resources.cache.period=0'. 3) For production, use content-based versioning: 'spring.web.resources.chain.strategy.content.enabled=true'. 4) Add version query parameters to static resource URLs. 5) Configure Cache-Control headers explicitly: 'spring.web.resources.cache.cachecontrol.no-cache=true'. 6) For CDN deployments, invalidate the cache after file updates. 7) Use build-time file hashing: 'app.abc123.js' instead of 'app.js'.",
        "difficulty": "Easy"
    },
]

# ====== CATEGORY 23: Health Check & Actuator Issues ======
health_scenarios = [
    {
        "question": "Spring Boot Actuator /actuator/health shows 'DOWN' status but the application is serving requests normally. The health indicator for a non-critical dependency is failing.",
        "answer": "1) Identify which health indicator is failing: check '/actuator/health' with 'management.endpoint.health.show-details=always'. 2) For non-critical dependencies, mark the indicator as non-critical: '@HealthIndicator' with 'statusAggregator'. 3) Use 'management.health.defaults.enabled=false' to disable default health indicators selectively. 4) Create a custom HealthIndicator that returns 'Status.UP' for non-critical failures. 5) Use 'management.health.db.enabled=false' if database health isn't critical. 6) Configure separate liveness and readiness probes: 'management.health.probes.enabled=true'. 7) Use 'management.endpoint.health.group.readiness.include=db,redis' for custom health groups.",
        "difficulty": "Medium"
    },
    {
        "question": "Spring Boot Actuator endpoints are not accessible at /actuator - all return 404. The spring-boot-starter-actuator dependency is included.",
        "answer": "1) Endpoints are not exposed by default - configure 'management.endpoints.web.exposure.include=*' or specific endpoints. 2) Check if 'management.endpoints.web.base-path' is customized from '/actuator'. 3) Verify the actuator dependency is on the classpath: 'mvn dependency:tree | grep actuator'. 4) Check if Spring Security is blocking access to /actuator/** paths. 5) For custom management port, access via 'http://host:management-port/actuator'. 6) Verify 'management.server.port' isn't set to a different port. 7) Check application logs for actuator auto-configuration issues.",
        "difficulty": "Easy"
    },
]

# ====== CATEGORY 24: Threading & Concurrency Issues ======
threading_scenarios = [
    {
        "question": "Spring Boot application's Tomcat threads are all in WAITING state. No new requests are being processed despite the application being healthy.",
        "answer": "1) Use 'jstack <pid>' to analyze thread dumps and find what threads are waiting for. 2) Check for database connection pool exhaustion - threads waiting for connections. 3) Look for deadlocks in the thread dump - 'jstack' reports them automatically. 4) Check if external service calls are timing out without proper timeout configuration. 5) Monitor thread pool metrics: '/actuator/metrics/tomcat.threads.current'. 6) Increase thread pool size: 'server.tomcat.threads.max=400' (default is 200). 7) Implement circuit breakers for external calls to fail fast instead of waiting. 8) Check for blocking operations in reactive code.",
        "difficulty": "Hard"
    },
    {
        "question": "Spring Boot application using CompletableFuture for parallel processing shows degraded performance compared to sequential execution. Thread pool is configured with 10 threads.",
        "answer": "1) Check if tasks are I/O-bound or CPU-bound - thread pool size should match the workload type. 2) For I/O-bound tasks, use more threads than CPU cores. For CPU-bound, use CPU cores + 1. 3) Verify the custom executor is being used: 'CompletableFuture.supplyAsync(task, customExecutor)'. 4) Check for thread contention - synchronized blocks or locks causing serialization. 5) Monitor thread pool utilization with Actuator metrics. 6) Use 'CompletableFuture.allOf()' correctly - don't block on individual futures. 7) Consider using virtual threads (Java 21+) for high-concurrency I/O workloads.",
        "difficulty": "Hard"
    },
]

# ====== CATEGORY 25: Miscellaneous Production Issues ======
misc_scenarios = [
    {
        "question": "Spring Boot application works in staging but fails in production with 'java.net.UnknownHostException' for an internal service name. The service is running and accessible from other pods.",
        "answer": "1) Check DNS configuration in the production environment - service name resolution may differ. 2) For Kubernetes, verify the service name includes the namespace: 'service-name.namespace.svc.cluster.local'. 3) Check if CoreDNS/kube-dns is running and healthy. 4) Verify the service selector matches the pod labels. 5) Test DNS resolution from within the pod: 'nslookup service-name'. 6) Check if network policies are blocking DNS queries. 7) For cross-cluster communication, use external DNS or service mesh (Istio).",
        "difficulty": "Medium"
    },
    {
        "question": "Spring Boot application's response times spike every day at the same time. The pattern repeats daily regardless of traffic volume.",
        "answer": "1) Check for scheduled tasks running at that time - @Scheduled jobs, cron jobs, or batch processes. 2) Look for database maintenance tasks (backups, vacuum, index rebuilds) at that time. 3) Check if log rotation is causing I/O spikes. 4) Monitor GC activity - scheduled full GC could cause pauses. 5) Check if a competing process on the same host is consuming resources. 6) Review cloud provider metrics - scheduled snapshots or backups. 7) Use APM tools (New Relic, Datadog) to correlate the spike with specific operations.",
        "difficulty": "Medium"
    },
    {
        "question": "Spring Boot application behind an Nginx reverse proxy shows wrong client IP addresses in logs. All requests appear to come from 127.0.0.1.",
        "answer": "1) Nginx forwards requests to localhost - the app sees the proxy's IP, not the client's. 2) Configure Nginx to forward the real IP: 'proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;'. 3) In Spring Boot, set 'server.forward-headers-strategy=native' or 'framework'. 4) Use 'X-Forwarded-For' header to get the real client IP: 'request.getHeader('X-Forwarded-For')'. 5) For Tomcat, configure RemoteIpValve: 'server.tomcat.remoteip.remote-ip-header=X-Forwarded-For'. 6) Use 'HttpServletRequest.getRemoteAddr()' with ForwardedHeaderFilter. 7) For accurate logging, configure logback to use '%{X-Forwarded-For}i' pattern.",
        "difficulty": "Medium"
    },
    {
        "question": "Spring Boot application's SSL/TLS certificate expires and the application stops accepting HTTPS connections. How do you implement automatic certificate renewal?",
        "answer": "1) Use Let's Encrypt with certbot for automatic renewal: 'certbot renew --deploy-hook 'systemctl restart myapp''. 2) For Kubernetes, use cert-manager with Let's Encrypt issuer. 3) Place a reverse proxy (Nginx, Traefik) in front and manage SSL at the proxy level. 4) Use AWS ACM or cloud provider's certificate manager with auto-renewal. 5) Monitor certificate expiry with Actuator health check or external monitoring. 6) For embedded Tomcat, implement a custom SSL connector that reloads certificates. 7) Set up alerts 30 days before expiry using 'openssl x509 -enddate' check.",
        "difficulty": "Hard"
    },
    {
        "question": "Spring Boot application with embedded Tomcat shows 'Too many open files' error under load. The OS file descriptor limit is 1024.",
        "answer": "1) Increase the file descriptor limit: 'ulimit -n 65536' (temporary) or edit '/etc/security/limits.conf' (permanent). 2) For systemd services, add 'LimitNOFILE=65536' in the service unit file. 3) Check for file descriptor leaks - unclosed InputStreams, FileOutputStreams, or database connections. 4) Use 'lsof -p <pid> | wc -l' to count open file descriptors. 5) Configure Tomcat's max connections: 'server.tomcat.max-connections=10000'. 6) Use try-with-resources for all I/O operations. 7) Monitor open file descriptors with Actuator and OS-level monitoring.",
        "difficulty": "Medium"
    },
]

# ============================================================
# COMBINE ALL SCENARIOS
# ============================================================
all_scenarios = (
    startup_scenarios + database_scenarios + rest_scenarios +
    security_scenarios + microservices_scenarios + performance_scenarios +
    config_scenarios + testing_scenarios + logging_scenarios +
    deployment_scenarios + exception_scenarios + transaction_scenarios +
    cache_scenarios + async_scenarios + build_scenarios +
    component_scenarios + gateway_scenarios + migration_scenarios +
    i18n_scenarios + websocket_scenarios + email_scenarios +
    file_scenarios + health_scenarios + threading_scenarios +
    misc_scenarios
)

print(f"Base scenarios: {len(all_scenarios)}")

# ============================================================
# GENERATE 1000 QUESTIONS by varying the base scenarios
# ============================================================

# Additional context variations to make each question unique
context_variations = [
    "In a high-traffic e-commerce platform",
    "During a production incident at 2 AM",
    "After a major version upgrade",
    "In a multi-tenant SaaS application",
    "When handling Black Friday traffic spikes",
    "In a microservices architecture with 15 services",
    "During a zero-downtime deployment",
    "In a regulated financial services environment",
    "After migrating from monolith to microservices",
    "In a Kubernetes cluster with auto-scaling",
    "When the team is under SLA pressure",
    "In a legacy system being modernized",
    "During a security audit",
    "In a real-time data processing pipeline",
    "When integrating with a third-party API",
    "In a multi-region deployment setup",
    "After a database migration from MySQL to PostgreSQL",
    "In a serverless-adjacent architecture",
    "When the monitoring system alerts at 3 AM",
    "During a compliance certification process",
    "In a CI/CD pipeline with automated deployments",
    "When onboarding a new team member",
    "In a disaster recovery scenario",
    "After a failed rolling update",
    "In a blue-green deployment setup",
    "When handling GDPR data deletion requests",
    "In a real-time analytics dashboard backend",
    "During a load testing exercise",
    "In a hybrid cloud environment",
    "After a network partition event",
    "In an event-driven architecture",
    "When dealing with eventual consistency",
    "In a CQRS-based system",
    "During a canary deployment",
    "In a service mesh environment with Istio",
    "When implementing SRE practices",
    "In a multi-cloud deployment strategy",
    "After a ransomware incident recovery",
    "In a PCI-DSS compliant environment",
    "When scaling from 100 to 10000 users",
]

# Additional technical details to vary answers
answer_additions = [
    " Document the root cause and resolution in the team's runbook.",
    " Set up automated alerts to catch this issue earlier next time.",
    " Add integration tests to prevent regression.",
    " Create a post-mortem document for the team.",
    " Update the team's troubleshooting playbook with this scenario.",
    " Consider adding automated health checks to detect this proactively.",
    " Review the monitoring dashboard to ensure this metric is tracked.",
    " Add this scenario to the on-call runbook.",
    " Implement automated remediation if possible.",
    " Schedule a team knowledge-sharing session on this topic.",
    " Add chaos engineering tests to validate the fix.",
    " Update the architecture decision record (ADR) if design changes.",
    " Review and update the incident response procedure.",
    " Add synthetic monitoring to detect this class of issues.",
    " Consider implementing feature flags for safer rollouts.",
]

questions = []
base_id = 8510  # Next ID after existing questions

# First, add all base scenarios as-is
for i, scenario in enumerate(all_scenarios):
    questions.append({
        "id": base_id + i,
        "topic": "Troubleshooting",
        "question": f"[Spring Boot] {scenario['question']}",
        "answer": scenario['answer'],
        "difficulty": scenario['difficulty']
    })

# Generate variations to reach 1000
remaining = 1000 - len(questions)
for i in range(remaining):
    base = all_scenarios[i % len(all_scenarios)]
    ctx = context_variations[i % len(context_variations)]
    addition = answer_additions[i % len(answer_additions)]
    
    questions.append({
        "id": base_id + len(questions),
        "topic": "Troubleshooting",
        "question": f"[Spring Boot] {ctx}: {base['question']}",
        "answer": base['answer'] + addition,
        "difficulty": base['difficulty']
    })

print(f"Total generated: {len(questions)}")

# Load existing questions and append
with open('/Users/shailabsingh/Desktop/interviewQues/questions.json', 'r') as f:
    existing = json.load(f)

existing.extend(questions)

# Re-verify IDs are unique
ids = [q['id'] for q in existing]
assert len(ids) == len(set(ids)), "Duplicate IDs found!"

with open('/Users/shailabsingh/Desktop/interviewQues/questions.json', 'w') as f:
    json.dump(existing, f, indent=2)

print(f"Done! Total questions in file: {len(existing)}")
print(f"New Troubleshooting questions added: {len(questions)}")
troubleshooting_count = sum(1 for q in existing if q['topic'] == 'Troubleshooting')
print(f"Total Troubleshooting questions: {troubleshooting_count}")
