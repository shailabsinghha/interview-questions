import json

questions = []

# --- SECURITY (40) ---
security_scenarios = [
    {
        "q": "Your Spring Boot application is behind a reverse proxy (Nginx). Users' IP addresses are showing up as the proxy's IP. How do you fix this to get the real client IP for auditing?",
        "a": "Configure 'server.forward-headers-strategy=native' in application.properties and ensure Nginx sends X-Forwarded-For headers. Spring Security will then use the RemoteIpFilter to populate the client IP.",
        "d": "Medium"
    },
    {
        "q": "You need to implement a 'remember-me' feature that persists across server restarts without using a database. How would you configure this in Spring Security?",
        "a": "Use TokenBasedRememberMeServices with a consistent key. Note: This is less secure than PersistentTokenBasedRememberMeServices (which uses a DB) because if the key is leaked, all tokens can be forged.",
        "d": "Medium"
    },
    {
        "q": "A security audit found that your JWTs are vulnerable to 'None' algorithm attacks. How do you prevent this in your Spring Security configuration?",
        "a": "Explicitly define the allowed algorithms in your JwtDecoder (e.g., NimbusJwtDecoder.withPublicKey(key).signatureAlgorithm(SignatureAlgorithm.RS256).build()) and reject any token without a signature or with the 'none' header.",
        "d": "Hard"
    },
    {
        "q": "Your microservice architecture requires sharing user context across services. How do you propagate a JWT from a Gateway to a downstream service using Spring Cloud Gateway?",
        "a": "Use the TokenRelay gateway filter. This filter extracts the JWT from the current authorized client and adds it as a Bearer token to the downstream request.",
        "d": "Medium"
    },
    {
        "q": "How would you implement 'Step-up Authentication' (e.g., requiring MFA only for high-value transactions) in a Spring Boot application?",
        "a": "Use Spring Security's expression-based access control or a custom Filter. When a user hits a sensitive endpoint, check if their Authentication object has the 'MFA_AUTHENTICATED' authority. If not, redirect to the MFA flow while preserving the original request.",
        "d": "Hard"
    },
    {
        "q": "Your application uses @PreAuthorize on service methods. You notice that unauthorized users get a 500 error instead of 403. Why is this happening and how do you fix it?",
        "a": "This happens if an AccessDeniedException is thrown inside the service layer but not caught by the FilterChain. Ensure you have @EnableWebSecurity and that Spring Security's exception translation filter is correctly configured to catch this and convert it to a 403 Forbidden.",
        "d": "Medium"
    },
    {
        "q": "Implement a custom AuthenticationProvider to authenticate users against a legacy COBOL system API. What core methods must you override?",
        "a": "Override authenticate(Authentication authentication) to perform the external API call and check credentials. Override supports(Class<?> authentication) to return true for your specific Authentication token type (e.g., UsernamePasswordAuthenticationToken).",
        "d": "Medium"
    },
    {
        "q": "You want to prevent users from logging in from multiple devices simultaneously. How do you configure concurrent session control in Spring Security?",
        "a": "Configure 'http.sessionManagement().maximumSessions(1).maxSessionsPreventsLogin(true)'. This requires a SessionRegistry bean and a HttpSessionEventPublisher to track session lifecycles correctly.",
        "d": "Medium"
    },
    {
        "q": "Your API is being scraped. You want to implement a dynamic IP-based rate limiter using Spring Security without using an external library. How would you do it?",
        "a": "Implement a custom Filter that sits before the authentication filter. Use a ConcurrentHashMap or a local Cache (like Caffeine) to track request counts per IP. If the limit is exceeded, throw a custom Exception or return a 429 Too Many Requests response directly.",
        "d": "Hard"
    },
    {
        "q": "How do you handle CSRF protection for a stateless REST API using Spring Security?",
        "a": "For stateless APIs using JWT, CSRF is often disabled (csrf().disable()) because the token is stored in local storage and not automatically sent by the browser. However, if using cookies for JWT, you should use CookieCsrfTokenRepository.withHttpOnlyFalse() and require a custom X-XSRF-TOKEN header.",
        "d": "Medium"
    },
    {
        "q": "Explain the vulnerability of storing JWTs in LocalStorage versus HttpOnly cookies and how Spring Boot handles both.",
        "a": "LocalStorage is vulnerable to XSS; HttpOnly cookies are vulnerable to CSRF. Spring Security facilitates cookie-based storage via CookieClearingLogoutHandler and custom filters, while LocalStorage requires manual header handling in controllers/filters.",
        "d": "Medium"
    },
    {
        "q": "You need to implement Role-Based Access Control (RBAC) where roles are fetched from a separate 'Permissions Service'. How do you integrate this into the Spring Security lifecycle?",
        "a": "Implement a custom UserDetailsService or a custom AuthenticationFilter. After the initial authentication, call the Permissions Service and populate the GrantedAuthority list in the Authentication object with the returned roles.",
        "d": "Hard"
    },
    {
        "q": "Your application needs to support both OAuth2 Social Login and local Username/Password login. How do you configure multiple security filter chains?",
        "a": "Define two @Bean SecurityFilterChain instances. Use @Order to prioritize them. Use request matchers (e.g., securityMatcher('/api/**')) to determine which chain handles which request.",
        "d": "Hard"
    },
    {
        "q": "In an OAuth2 Resource Server, you want to map a custom claim from the JWT (e.g., 'user_id') to the Principal object in Spring Security. How is this achieved?",
        "a": "Configure a custom JwtAuthenticationConverter. Override the 'convert' method to extract the claim from the Jwt object and create a new AbstractAuthenticationToken (like JwtAuthenticationToken) with the custom principal.",
        "d": "Medium"
    },
    {
        "q": "How would you implement a 'Graceful Shutdown' in Spring Security to ensure active sessions aren't immediately killed during a redeploy?",
        "a": "Enable 'server.shutdown=graceful' (Spring Boot 2.3+). This allows the web server to stop accepting new requests while finishing active ones. Use a distributed session store (Spring Session Redis) so that session state persists across different instances.",
        "d": "Medium"
    },
    {
        "q": "You want to encrypt sensitive fields (like SSN) in your database using Spring Data JPA. What is the most seamless way to do this?",
        "a": "Use a JPA AttributeConverter. Implement 'convertToDatabaseColumn' (using AES encryption) and 'convertToEntityAttribute' (decryption). Annotate the SSN field with @Convert(converter = MyEncryptionConverter.class).",
        "d": "Medium"
    },
    {
        "q": "Your Spring Boot app is failing the OWASP Top 10 check for 'Insecure Headers'. How do you quickly add Security Headers like HSTS, Content-Security-Policy, and X-Frame-Options?",
        "a": "Spring Security adds these by default. If you need to customize them, use 'http.headers().contentSecurityPolicy(...)', 'http.headers().httpStrictTransportSecurity(...)', etc., in your SecurityFilterChain bean.",
        "d": "Easy"
    },
    {
        "q": "How do you implement Method Security that checks if the 'Owner' of a resource is the one trying to modify it?",
        "a": "Use @PreAuthorize(\"@securityService.isOwner(authentication, #id)\"). Create a 'securityService' bean that looks up the resource by ID and compares the owner field with the authenticated user's name.",
        "d": "Medium"
    },
    {
        "q": "A user is locked out after 5 failed login attempts. How do you implement this 'Account Locking' logic using Spring Security events?",
        "a": "Register an ApplicationListener for AuthenticationFailureBadCredentialsEvent. In the listener, increment a counter in the database. Once the limit is reached, set 'accountNonLocked=false' in the UserDetails entity.",
        "d": "Medium"
    },
    {
        "q": "How do you handle authentication for a WebSocket connection that uses STOMP in Spring Boot?",
        "a": "STOMP doesn't support standard HTTP headers for authentication after the handshake. You must use a ChannelInterceptor to intercept the CONNECT message and extract credentials (like a JWT) from the native headers.",
        "d": "Hard"
    },
    {
        "q": "You want to log every single request and its associated user ID for security auditing. Where is the best place to implement this?",
        "a": "Use a OncePerRequestFilter. Since the SecurityContext is populated by earlier filters, you can access SecurityContextHolder.getContext().getAuthentication() to get the user, and then log the request details.",
        "d": "Medium"
    },
    {
        "q": "Your application needs to support 'Impersonation' (Admin acting as a User). How does Spring Security support this?",
        "a": "Use the SwitchUserFilter. It allows an admin to navigate to '/login/impersonate?username=user1'. Spring Security replaces the current authentication with the targeted user while keeping the original admin info in a 'ROLE_PREVIOUS_ADMINISTRATION' authority.",
        "d": "Hard"
    },
    {
        "q": "Explain how to protect against Brute Force attacks on your login endpoint using a 'Login Delay' strategy.",
        "a": "In your custom AuthenticationProvider or UserDetailsService, if authentication fails, use Thread.sleep(randomDelay) or a more sophisticated throttling mechanism to slow down subsequent attempts for that specific username/IP.",
        "d": "Medium"
    },
    {
        "q": "In a multitenant application, how do you ensure that a user from Tenant A cannot access resources from Tenant B, even if they have the correct ID?",
        "a": "Implement a TenantFilter that extracts the tenant ID from the request (header/subdomain). Store it in a ThreadLocal (TenantContext). In your repository layer, use a Hibernate @Filter or JPA @PostLoad check to enforce the tenant boundary.",
        "d": "Hard"
    },
    {
        "q": "How do you secure your Spring Boot Actuator endpoints so only 'ADMIN' users can see them, but 'metrics' are public?",
        "a": "In your SecurityFilterChain, use: 'requestMatchers(\"/actuator/metrics\").permitAll()' and 'requestMatchers(\"/actuator/**\").hasRole(\"ADMIN\")'. Ensure 'management.endpoints.web.exposure.include' is also configured.",
        "d": "Easy"
    },
    {
        "q": "Your JWT has expired, and the client receives a 401. How do you implement a 'Refresh Token' flow to get a new JWT without the user re-logging?",
        "a": "Implement a '/refresh' endpoint that accepts a Refresh Token (stored in a database). If valid, generate a new JWT and a new Refresh Token (rotating tokens). Use 'OncePerRequestFilter' to handle JWT expiration gracefully.",
        "d": "Medium"
    },
    {
        "q": "You are using Spring Security with OAuth2 Client. How do you access the authorized client's access token in a Controller?",
        "a": "Inject '@RegisteredOAuth2AuthorizedClient(\"client-registration-id\") OAuth2AuthorizedClient authorizedClient' into your controller method. You can then call 'authorizedClient.getAccessToken().getTokenValue()'.",
        "d": "Medium"
    },
    {
        "q": "How do you implement Cross-Origin Resource Sharing (CORS) in Spring Boot such that only your frontend domain can access the API?",
        "a": "Define a 'WebMvcConfigurer' bean and override 'addCorsMappings'. Use 'registry.addMapping(\"/**\").allowedOrigins(\"https://myapp.com\").allowedMethods(\"GET\", \"POST\", ...)'.",
        "d": "Easy"
    },
    {
        "q": "Explain the difference between @Secured, @PreAuthorize, and @RolesAllowed in Spring Security.",
        "a": "@Secured is Spring-specific (legacy). @RolesAllowed is the JSR-250 standard. @PreAuthorize is the most powerful, supporting SpEL (Spring Expression Language) for complex logic (e.g., checking method arguments).",
        "d": "Easy"
    },
    {
        "q": "How do you prevent 'Timing Attacks' during password verification in Spring Security?",
        "a": "Spring Security's BCryptPasswordEncoder (and others) are designed to be time-constant for a given workload. It always performs the full hashing process even if the user doesn't exist, preventing attackers from guessing existence based on response time.",
        "d": "Hard"
    },
    {
        "q": "You want to hide the password field from being serialized in JSON responses. How do you do this globally?",
        "a": "Use @JsonProperty(access = JsonProperty.Access.WRITE_ONLY) on the password field in your Entity/DTO. This ensures it's accepted during deserialization (POST) but never sent during serialization (GET).",
        "d": "Easy"
    },
    {
        "q": "How do you implement 'LDAP Authentication' in Spring Boot for an enterprise environment?",
        "a": "Add 'spring-boot-starter-data-ldap' and 'spring-security-ldap'. Configure 'ldap.urls', 'ldap.base', and 'ldap.user.dn-pattern'. In SecurityConfig, use 'auth.ldapAuthentication().userDnPatterns(...).groupSearchBase(...)'.",
        "d": "Medium"
    },
    {
        "q": "Your app uses a self-signed certificate for HTTPS. RestTemplate calls are failing with 'SSLHandshakeException'. How do you fix this for development?",
        "a": "Create a custom RestTemplate bean that uses a CloseableHttpClient configured with a SSLContext that trusts all certificates (or your specific self-signed cert). Never do 'trust all' in production.",
        "d": "Medium"
    },
    {
        "q": "How do you implement 'API Key' authentication (passing a key in the header) alongside standard session-based auth?",
        "a": "Create a custom filter that checks the 'X-API-KEY' header. If present, it creates an Authentication object and places it in the SecurityContext. Insert this filter before the 'UsernamePasswordAuthenticationFilter'.",
        "d": "Medium"
    },
    {
        "q": "How does Spring Security protect against Session Fixation?",
        "a": "By default, Spring Security changes the Session ID upon successful authentication (SessionFixationProtectionStrategy). This ensures that a session ID obtained before login cannot be used after login.",
        "d": "Medium"
    },
    {
        "q": "You need to store passwords using a pepper (a secret key known only to the server) in addition to a salt. How do you implement this?",
        "a": "Spring Security's standard encoders don't support peppers natively. You would need to create a custom PasswordEncoder implementation that concatenates the password with the pepper before passing it to BCrypt.",
        "d": "Hard"
    },
    {
        "q": "Explain 'Scope-based' authorization in OAuth2. How do you check for a scope in a Spring Boot controller?",
        "a": "Scopes are represented as authorities with the 'SCOPE_' prefix. You can use @PreAuthorize(\"hasAuthority('SCOPE_read')\") or check the authorities list in the principal.",
        "d": "Medium"
    },
    {
        "q": "How do you implement 'Silent Authentication' in an OIDC flow with Spring Boot?",
        "a": "Use the 'prompt=none' parameter in the authorization request. This tells the IDP to only return a token if the user is already authenticated, otherwise return an error. Spring Security handles this via customized AuthorizationRequestResolvers.",
        "d": "Hard"
    },
    {
        "q": "Your application needs to handle multiple password encoding formats (e.g., migrating from MD5 to BCrypt). How does Spring Security help?",
        "a": "Use DelegatingPasswordEncoder. It stores the password with a prefix like '{bcrypt}encodedPassword'. When checking, it looks at the prefix to decide which encoder to use. This allows seamless migration as users log in.",
        "d": "Medium"
    },
    {
        "q": "How would you implement 'Two-Factor Authentication' (2FA) where the second factor is a TOTP (Google Authenticator)?",
        "a": "After the first successful login, redirect the user to a '2fa' page. Store the authentication in a temporary 'partial' state. Use a library like 'google-auth' to verify the TOTP code. If valid, promote the user to a fully authenticated state.",
        "d": "Hard"
    }
]

# --- PERSISTENCE (40) ---
persistence_scenarios = [
    {
        "q": "You have a large batch update process that is very slow. You are using JPA's saveAll(). How can you improve performance using JDBC batching?",
        "a": "Set 'spring.jpa.properties.hibernate.jdbc.batch_size=50' and 'spring.jpa.properties.hibernate.order_inserts=true'. Also, ensure you are using 'GenerationType.SEQUENCE' (or IDENTITY with 'rewriteBatchedStatements=true' for MySQL) to allow batching.",
        "d": "Medium"
    },
    {
        "q": "You notice 'LazyInitializationException' when accessing a child collection in a Thymeleaf template. How do you solve this without using 'Open Session in View'?",
        "a": "Use a Join Fetch in your JPQL query (e.g., 'SELECT p FROM Parent p JOIN FETCH p.children') or use an @EntityGraph to specify which collections should be eagerly loaded for that specific request.",
        "d": "Medium"
    },
    {
        "q": "Explain the difference between @Transactional(propagation = Propagation.REQUIRED) and REQUIRES_NEW. Give a scenario for each.",
        "a": "REQUIRED (default) joins an existing transaction. REQUIRES_NEW always starts a new transaction, suspending the current one. Use REQUIRES_NEW for logging or auditing where you want the log to persist even if the main transaction fails.",
        "d": "Medium"
    },
    {
        "q": "How do you implement 'Optimistic Locking' in Spring Data JPA to prevent lost updates in a concurrent environment?",
        "a": "Add a @Version field (Long or Timestamp) to your entity. JPA will automatically check if the version hasn't changed before updating. If it has, it throws an ObjectOptimisticLockingFailureException.",
        "d": "Easy"
    },
    {
        "q": "You need to perform a 'Pessimistic Lock' on a database row to prevent any other thread from reading or writing while a price update happens. How do you do this in Spring Data JPA?",
        "a": "Annotate your repository method with @Lock(LockModeType.PESSIMISTIC_WRITE). This will add 'FOR UPDATE' to the SQL query (in most DBs), locking the row until the transaction completes.",
        "d": "Medium"
    },
    {
        "q": "Your application uses @GeneratedValue(strategy = GenerationType.AUTO). Why is this generally avoided in production and what is the preferred alternative?",
        "a": "AUTO lets Hibernate decide the strategy, which often results in 'hibernate_sequence' table (global sequence), causing contention. Use SEQUENCE (for PostgreSQL/Oracle) or IDENTITY (for MySQL/SQL Server) for better performance and predictability.",
        "d": "Easy"
    },
    {
        "q": "You have a complex query that involves multiple joins and dynamic filters. Should you use JPQL, Criteria API, or Querydsl? Justify.",
        "a": "Querydsl or Criteria API are better for dynamic filters as they provide type-safety and prevent string concatenation errors. JPQL is fine for static queries but becomes brittle with many 'if' statements for dynamic parts.",
        "d": "Medium"
    },
    {
        "q": "Explain 'Soft Deletes' in JPA. How do you implement it so that 'findAll()' automatically excludes deleted records?",
        "a": "Add a boolean 'deleted' field. Annotate the entity with @SQLDelete(sql = \"UPDATE table SET deleted = true WHERE id = ?\") and @Where(clause = \"deleted = false\").",
        "d": "Medium"
    },
    {
        "q": "You have a @OneToMany relationship where the parent has 10,000 children. Fetching the parent takes forever. How do you implement pagination for the children?",
        "a": "Do not use the collection directly. Instead, create a separate repository method for the children that takes the parent ID and a Pageable object (e.g., 'findByParentId(Long parentId, Pageable pageable)').",
        "d": "Medium"
    },
    {
        "q": "What is the 'N+1 Select Problem' and how can you detect it in a Spring Boot application during development?",
        "a": "N+1 happens when you fetch N parent records, and then Hibernate fires N additional queries to fetch children for each. Detect it by enabling 'spring.jpa.show-sql=true' or using a tool like 'hypersistence-utils' which can throw exceptions if more than X queries are fired per session.",
        "d": "Easy"
    },
    {
        "q": "How do you implement a 'Read-Only' transaction in Spring Boot and why is it beneficial?",
        "a": "@Transactional(readOnly = true). It optimizes Hibernate by disabling dirty checking (objects aren't checked for changes), potentially routing the query to a read-replica database if configured.",
        "d": "Easy"
    },
    {
        "q": "You need to map a JSONB column in PostgreSQL to a Java Map or POJO. How is this achieved with Hibernate?",
        "a": "Use a custom Type (UserType) or a library like 'hypersistence-utils'. Annotate the field with @Type(type = \"jsonb\") after registering the type in the package-info.java or using @TypeDef.",
        "d": "Hard"
    },
    {
        "q": "Explain 'Entity Lifecycle Listeners' in JPA. Give a scenario where @PrePersist would be useful.",
        "a": "These are callbacks (@PrePersist, @PostUpdate, etc.). @PrePersist is perfect for automatically setting 'createdAt' or 'lastModifiedAt' timestamps before the entity is saved for the first time.",
        "d": "Easy"
    },
    {
        "q": "You want to use a Database View instead of a Table for one of your JPA entities. Is this possible? If so, how?",
        "a": "Yes, just annotate the class with @Entity and @Table(name = \"my_view_name\"). Note: Views are usually read-only, so you might want to annotate the entity with @Immutable or be careful with save() operations.",
        "d": "Medium"
    },
    {
        "q": "Explain the 'First Level Cache' in Hibernate. Does it persist across multiple web requests?",
        "a": "No, the First Level Cache (Persistence Context) is bound to the Session (usually one web request/transaction). It ensures that within the same session, calling findById twice for the same entity returns the same instance without a second DB hit.",
        "d": "Easy"
    },
    {
        "q": "How do you configure a 'Second Level Cache' (e.g., using Ehcache or Redis) in a Spring Boot application?",
        "a": "Enable it in properties: 'spring.jpa.properties.hibernate.cache.use_second_level_cache=true'. Specify the provider: 'spring.jpa.properties.hibernate.cache.region.factory_class=...'. Annotate entities with @Cacheable.",
        "d": "Medium"
    },
    {
        "q": "You are getting 'TransactionTimedOutException' for a long-running report. How do you increase the timeout for a specific @Transactional method?",
        "a": "Use '@Transactional(timeout = 60)' (value in seconds). Ensure the underlying database and transaction manager also support this timeout.",
        "d": "Easy"
    },
    {
        "q": "Describe how to implement Multi-Tenancy using a 'Schema-per-Tenant' strategy in Spring Boot.",
        "a": "Implement 'CurrentTenantIdentifierResolver' to get the tenant ID (from context) and 'MultiTenantConnectionProvider' to provide a connection to the correct schema. Configure these in Hibernate properties.",
        "d": "Hard"
    },
    {
        "q": "You need to call a Database Stored Procedure that returns multiple result sets. How do you handle this in JPA?",
        "a": "Use @NamedStoredProcedureQuery or the EntityManager's 'createStoredProcedureQuery' method. You'll need to use 'execute()' and then 'getResultSetList()' or 'getNextResultSet()'.",
        "d": "Hard"
    },
    {
        "q": "What is the difference between 'FetchType.LAZY' and 'FetchType.EAGER'? Why is LAZY usually preferred for collections?",
        "a": "EAGER loads the data immediately. LAZY loads it only when accessed. LAZY is preferred for collections to avoid loading thousands of related objects unnecessarily, which causes massive memory usage and slow response times.",
        "d": "Easy"
    },
    {
        "q": "How do you implement 'Audit Logging' (who changed what and when) in Spring Data JPA without writing manual log code?",
        "a": "Use Spring Data Envers. Annotate your entities with @Audited. It will automatically create '_AUD' tables and track every change. Use AuditReader to query the history.",
        "d": "Medium"
    },
    {
        "q": "You have an entity that is rarely updated but frequently read. How do you optimize its retrieval using Hibernate's Query Cache?",
        "a": "Enable Query Cache in properties. In your repository, use '@QueryHints(@QueryHint(name = \"org.hibernate.cacheable\", value = \"true\"))'. This caches the results of the specific query, not just the entities.",
        "d": "Medium"
    },
    {
        "q": "How do you handle 'Deadlocks' in a Spring Boot application that performs many concurrent database updates?",
        "a": "Use a retry mechanism (e.g., Spring Retry) on the service method. Implement a consistent ordering for updates (always update Table A then Table B) to prevent circular waits. Reduce transaction size.",
        "d": "Hard"
    },
    {
        "q": "Explain 'Projection' in Spring Data JPA. When would you use a 'Closed Projection' (Interface) vs a 'DTO Projection'?",
        "a": "Projections allow fetching only specific columns. Use Interface projections for simplicity (Spring generates proxy). Use DTO projections (Constructor expression in @Query) for better performance and easier testing, as it avoids proxy overhead.",
        "d": "Medium"
    },
    {
        "q": "You need to use multiple DataSources (one for MySQL, one for MongoDB). How do you configure Spring Boot to handle this?",
        "a": "Define two sets of configurations. Create separate @Configuration classes for each. Use @EnableJpaRepositories and @EnableMongoRepositories, pointing each to its specific package and TransactionManager/Template bean.",
        "d": "Hard"
    },
    {
        "q": "How do you perform a 'Bulk Delete' in Spring Data JPA that bypasses the Persistence Context (and thus lifecycle hooks)?",
        "a": "Use a @Modifying @Query (e.g., '@Query(\"DELETE FROM Entity e WHERE e.status = :status\")'). This executes a single SQL delete instead of loading each entity and deleting it individually.",
        "d": "Medium"
    },
    {
        "q": "Explain the 'Object-Relational Mapping' of an Inheritance hierarchy using the 'SINGLE_TABLE' strategy. What is the 'Discriminator' column?",
        "a": "All classes in the hierarchy are stored in one table. The Discriminator column (e.g., 'dtype') stores a value indicating which subclass a specific row represents. Pros: fast polymorphic queries. Cons: many nullable columns.",
        "d": "Medium"
    },
    {
        "q": "How do you use 'Spring Data JPA Specifications' to implement a search API with optional filters (e.g., filter by name IF name is provided)?",
        "a": "Implement the Specification interface. In your service, build a Spec by combining predicates: 'if(name != null) spec = spec.and(hasName(name))'. Pass this Spec to the repository's 'findAll(spec)'.",
        "d": "Medium"
    },
    {
        "q": "You are getting 'ConstraintViolationException' but you want to provide a user-friendly message. How do you handle this globally?",
        "a": "Catch it in a @ControllerAdvice. Since it often wraps an underlying JDBC exception, you might need to inspect the root cause and map the specific constraint name (e.g., 'uk_user_email') to a friendly message like 'Email already exists'.",
        "d": "Medium"
    },
    {
        "q": "What is 'Dirty Checking' in Hibernate and how does it work?",
        "a": "Hibernate maintains a 'snapshot' of the entity when it's loaded. At the end of the transaction (flush time), it compares the current state with the snapshot. If they differ, it automatically generates and executes an UPDATE statement.",
        "d": "Easy"
    },
    {
        "q": "How do you map a @ManyToMany relationship with an extra column in the join table (e.g., 'created_at' in the user_roles table)?",
        "a": "You cannot use @ManyToMany directly. Instead, create a third entity (e.g., UserRole) that has @ManyToOne to User and @ManyToOne to Role. The extra columns go into this UserRole entity.",
        "d": "Medium"
    },
    {
        "q": "You need to execute a Native SQL query because JPQL doesn't support a specific database function. How do you map the result to a non-entity POJO?",
        "a": "Use @SqlResultSetMapping with @ConstructorResult. In your @Query, set 'nativeQuery = true'. This tells JPA how to map the raw columns to your POJO's constructor.",
        "d": "Hard"
    },
    {
        "q": "Explain 'FlushMode' in Hibernate. What is the difference between AUTO and COMMIT?",
        "a": "AUTO (default) flushes before every query to ensure the query sees current changes. COMMIT flushes only when the transaction is committed. COMMIT is faster but can lead to 'stale' data in queries within the same transaction.",
        "d": "Hard"
    },
    {
        "q": "How do you implement 'Pagination' in a native SQL query in Spring Data JPA?",
        "a": "For native queries, Spring Data doesn't automatically add 'LIMIT/OFFSET'. You must either write them manually in the SQL or provide a 'countQuery' and hope the dialect handles it. Better: use a named query or JPQL if possible.",
        "d": "Medium"
    },
    {
        "q": "You want to use 'UUID' as the Primary Key for your entities. How do you configure Hibernate to generate them automatically?",
        "a": "Annotate the ID field with '@GeneratedValue(generator = \"UUID\")' and '@GenericGenerator(name = \"UUID\", strategy = \"org.hibernate.id.UUIDGenerator\")'. Ensure the DB column type is compatible (e.g., 'uuid' in Postgres).",
        "d": "Easy"
    },
    {
        "q": "Explain 'Orphan Removal' in JPA. How is it different from 'CascadeType.REMOVE'?",
        "a": "CascadeType.REMOVE deletes children when the parent is deleted. orphanRemoval=true also deletes a child if it is simply removed from the parent's collection (e.g., parent.getChildren().remove(child1)).",
        "d": "Medium"
    },
    {
        "q": "How do you handle 'Database Migrations' in a Spring Boot application? Compare Liquibase and Flyway.",
        "a": "Both allow versioned SQL scripts. Flyway is simpler, using plain SQL. Liquibase is more powerful, using XML/YAML/JSON to describe changes, allowing for easier rollback and DB-agnostic migrations. Both integrate via 'spring-boot-starter'.",
        "d": "Easy"
    },
    {
        "q": "Explain the 'Open Session in View' (OSIV) pattern. Why is it enabled by default in Spring Boot, and why do many experts recommend disabling it?",
        "a": "OSIV keeps the Hibernate session open until the view is rendered, preventing LazyInitializationException. It's enabled for developer convenience. Experts disable it because it can lead to N+1 problems going unnoticed and hold onto DB connections too long.",
        "d": "Medium"
    },
    {
        "q": "How do you implement 'Sharding' with Spring Data JPA?",
        "a": "Spring Data JPA doesn't support sharding natively. You would usually use a middleware like Shardingsphere or Citus, or implement a custom AbstractRoutingDataSource that determines which shard to use based on a Sharding Key in the thread context.",
        "d": "Hard"
    },
    {
        "q": "What is the purpose of '@Modifying' annotation on repository methods?",
        "a": "It signals to Spring Data that the query is an INSERT, UPDATE, or DELETE operation rather than a SELECT. It ensures the query is executed via 'executeUpdate()' instead of 'executeQuery()'.",
        "d": "Easy"
    }
]

# --- MICROSERVICES (40) ---
microservice_scenarios = [
    {
        "q": "Your microservice architecture has 50+ services. How do you manage their configurations centrally so you don't have to redeploy for every property change?",
        "a": "Use Spring Cloud Config Server. Services fetch their properties on startup from a central Git/Vault repository. Use '@RefreshScope' and '/actuator/refresh' to update properties at runtime without restart.",
        "d": "Medium"
    },
    {
        "q": "How does 'Service Discovery' (e.g., Eureka) solve the problem of hardcoding IP addresses in a dynamic cloud environment?",
        "a": "Services register themselves with Eureka on startup with a service ID. Other services (clients) query Eureka using that ID to get the current list of healthy IP/ports. This allows scaling and handling instance failures automatically.",
        "d": "Easy"
    },
    {
        "q": "Explain the role of 'Spring Cloud Gateway'. How is it different from a traditional Load Balancer like Nginx?",
        "a": "Gateway is 'application-aware'. It can perform routing based on predicates (e.g., headers, paths), modify requests/responses via filters, and integrate with Spring Security for centralized auth. Nginx is faster for static content but Gateway is more flexible for Java-based logic.",
        "d": "Medium"
    },
    {
        "q": "How do you implement a 'Circuit Breaker' to prevent a failing downstream service from bringing down your entire system?",
        "a": "Use Resilience4j. Wrap the service call with '@CircuitBreaker(name = \"myService\", fallbackMethod = \"fallback\")'. If failures exceed a threshold, the circuit 'opens', and the fallback is immediately called instead of the failing service.",
        "d": "Medium"
    },
    {
        "q": "Explain the 'Saga Pattern'. When would you use 'Choreography' versus 'Orchestration'?",
        "a": "Saga manages distributed transactions. Choreography: each service emits events that trigger the next service (decentralized). Orchestration: a central orchestrator tells each service what to do (centralized control). Use Choreography for simple flows; Orchestration for complex ones.",
        "d": "Hard"
    },
    {
        "q": "How do you implement 'Distributed Tracing' in Spring Boot to see the full path of a request across 10 microservices?",
        "a": "Use Micrometer Tracing (formerly Spring Cloud Sleuth) and export data to Zipkin or Jaeger. It injects a 'traceId' into logs and headers, allowing you to stitch together the entire request lifecycle.",
        "d": "Medium"
    },
    {
        "q": "Your microservices need to communicate. When should you use 'Feign Client' vs 'RestTemplate'?",
        "a": "Feign is declarative; you just define an interface with annotations. It's much cleaner and integrates natively with Eureka and LoadBalancer. RestTemplate is imperative and more flexible but requires more boilerplate code.",
        "d": "Easy"
    },
    {
        "q": "Explain 'Sidecar Pattern'. How is it implemented in a Kubernetes environment with Spring Boot?",
        "a": "A sidecar is a separate container running alongside the app container (e.g., Envoy for service mesh). It handles cross-cutting concerns like logging, security, or proxying. In K8s, it's defined in the same Pod spec.",
        "d": "Medium"
    },
    {
        "q": "How do you handle 'Data Redundancy' in microservices? For example, the Order service needs the User's name, but the User's name is in the User service.",
        "a": "Avoid synchronous calls (N+1). Instead, use 'Eventual Consistency'. When a user's name changes, emit an event. The Order service listens and updates its own local 'User' cache or denormalized table.",
        "d": "Hard"
    },
    {
        "q": "What is 'Client-Side Load Balancing' (e.g., Spring Cloud LoadBalancer) and how does it differ from Server-Side LB?",
        "a": "Client-Side LB: The client (service) gets the list of all instances from Eureka and chooses one (Round Robin, etc.) itself. Server-Side LB: The client hits a single IP (like F5 or Nginx), which then decides where to route.",
        "d": "Medium"
    },
    {
        "q": "How do you implement 'Rate Limiting' at the API Gateway level to prevent a single user from overwhelming your system?",
        "a": "Use Spring Cloud Gateway's 'RedisRateLimiter'. It uses a Token Bucket algorithm. Configure 'replenishRate' (tokens per sec) and 'burstCapacity' in the route definition.",
        "d": "Medium"
    },
    {
        "q": "Describe the 'Backend for Frontend' (BFF) pattern. Why would a mobile app need a different BFF than a web app?",
        "a": "A BFF is a gateway tailored for a specific client. A mobile app might need minimized JSON payloads and aggregated responses to save battery/data, while a web app might want more detailed data for a large screen.",
        "d": "Medium"
    },
    {
        "q": "How do you handle 'API Versioning' in a microservice environment to avoid breaking existing clients?",
        "a": "Common strategies: URI versioning (/v1/users), Header versioning (Accept: application/vnd.myapp.v1+json), or Query parameter versioning. URI is the most common and easiest to cache/debug.",
        "d": "Easy"
    },
    {
        "q": "Explain 'Blue-Green Deployment'. How can you achieve this using Spring Boot and a Load Balancer?",
        "a": "Blue is current prod; Green is new version. Deploy Green alongside Blue. Once tested, switch the Load Balancer (or Gateway) to point to Green. If issues occur, switch back to Blue immediately.",
        "d": "Medium"
    },
    {
        "q": "What is 'Contract Testing' (e.g., Spring Cloud Contract) and why is it crucial for microservices?",
        "a": "It ensures that a Producer (Service A) doesn't break its Consumer (Service B) by changing the API. The producer provides a 'contract', and the consumer uses 'stubs' generated from that contract for its own tests.",
        "d": "Hard"
    },
    {
        "q": "How do you implement 'Health Checks' in Spring Boot so that Kubernetes knows when to restart a failing pod?",
        "a": "Use Spring Boot Actuator's '/actuator/health' endpoint. Kubernetes uses this for 'Liveness' (is it alive?) and 'Readiness' (is it ready to take traffic?) probes.",
        "d": "Easy"
    },
    {
        "q": "Explain 'CQRS' (Command Query Responsibility Segregation). When is it useful in a microservice architecture?",
        "a": "Separate models for Writing (Commands) and Reading (Queries). Useful when read patterns are very different from write patterns, allowing you to optimize a read-database (like Elasticsearch) separately from the write-database (PostgreSQL).",
        "d": "Hard"
    },
    {
        "q": "How do you secure communication between microservices? Explain 'mTLS'.",
        "a": "Mutual TLS (mTLS) requires both the client and server to present certificates. This ensures that only authorized services can talk to each other. Often handled by a Service Mesh (Istio/Linkerd) to avoid coding it in Java.",
        "d": "Hard"
    },
    {
        "q": "What is 'Externalized Configuration' and why is it one of the 12-factor app principles?",
        "a": "Keeping config (DB URLs, secrets) out of the code/artifact. This allows the same jar to run in Dev, QA, and Prod just by changing environment variables or using a config server.",
        "d": "Easy"
    },
    {
        "q": "How do you implement 'Auto-Scaling' for a Spring Boot service running in AWS ECS?",
        "a": "Configure a CloudWatch Alarm based on CPU or Memory usage. When the threshold is hit, it triggers an Application Auto Scaling policy to increase the 'desired count' of tasks in the ECS service.",
        "d": "Medium"
    },
    {
        "q": "Explain the 'Database-per-Service' pattern. What are its pros and cons?",
        "a": "Each service owns its data. Pros: loose coupling, independent scaling, technology choice. Cons: difficult distributed transactions, complex joins across services, data duplication.",
        "d": "Easy"
    },
    {
        "q": "How do you handle 'Logging' across 100 microservices? Describe an ELK or EFK stack.",
        "a": "Services send logs to Logstash/Fluentd. They are indexed in Elasticsearch and visualized in Kibana. Crucial to include 'traceId' in every log line to enable cross-service log correlation.",
        "d": "Medium"
    },
    {
        "q": "What is 'Service Mesh' (e.g., Istio) and how does it relate to Spring Cloud?",
        "a": "Istio handles networking concerns (discovery, retries, security) at the infrastructure level (sidecar). Spring Cloud does it at the application level (Java libraries). Many are moving to Istio to keep the Java code 'clean' of infra logic.",
        "d": "Hard"
    },
    {
        "q": "Explain 'Idempotency' in the context of retrying failed API calls. How do you implement it?",
        "a": "An operation is idempotent if multiple identical requests have the same effect as one. Implement by requiring an 'Idempotency-Key' header. Store the key and the previous response in a cache; if the key is seen again, return the cached response.",
        "d": "Medium"
    },
    {
        "q": "Your microservice is consuming too much memory in a container. How do you tune the 'JVM Memory Limits' for a Docker environment?",
        "a": "Use '-XX:MaxRAMPercentage=75.0' instead of '-Xmx'. This tells the JVM to take 75% of the container's allocated memory, preventing it from being killed by the Docker OOM killer.",
        "d": "Medium"
    },
    {
        "q": "How do you implement 'Feature Flags' in a Spring Boot microservice?",
        "a": "Use a library like LaunchDarkly or a simple DB-backed service. Wrap code in 'if(featureEnabled(\"new-ui\"))'. Allows turning features on/off without redeploying code.",
        "d": "Easy"
    },
    {
        "q": "Explain 'API Composition' vs 'API Gateway' for data aggregation.",
        "a": "API Composition: A service calls multiple other services and merges the results. API Gateway: The gateway itself performs the calls and aggregation. Gateway aggregation is faster for the client but can make the gateway a 'fat' monolith.",
        "d": "Medium"
    },
    {
        "q": "What is 'Zookeeper' and how is it used in microservices compared to Eureka?",
        "a": "Zookeeper is a general-purpose distributed coordination service (strong consistency). Eureka is specialized for service discovery (eventual consistency). Eureka is usually preferred for discovery because it's more resilient to network partitions.",
        "d": "Hard"
    },
    {
        "q": "How do you implement 'Shadow Deployment'? Why is it useful?",
        "a": "Route production traffic to the new version but discard its responses. Useful for testing performance and correctness against real-world traffic without impacting users.",
        "d": "Hard"
    },
    {
        "q": "Describe how 'Spring Cloud Bus' works to propagate configuration changes.",
        "a": "It links microservices with a message broker (RabbitMQ/Kafka). When a config change occurs, a single service receives a '/bus-refresh' call, and it broadcasts the event to all other services to refresh their config.",
        "d": "Medium"
    },
    {
        "q": "How do you handle 'Clock Skew' in a distributed system when using timestamps for ordering events?",
        "a": "Never rely on absolute timestamps for strict ordering. Use 'Logical Clocks' (Lamport timestamps) or 'Vector Clocks'. Alternatively, use a centralized sequencer or a DB with a global clock.",
        "d": "Hard"
    },
    {
        "q": "Explain 'Polyglot Persistence'. Give an example in a Spring Boot ecosystem.",
        "a": "Using different DBs for different needs. Example: User data in PostgreSQL (relational), Product catalog in MongoDB (flexible schema), and Search in Elasticsearch (full-text search).",
        "d": "Easy"
    },
    {
        "q": "What is 'Hystrix' and why is it in maintenance mode? What is the recommended replacement?",
        "a": "Hystrix was Netflix's circuit breaker library. It's in maintenance because it's complex and over-engineered for modern needs. The recommended replacement is Resilience4j, which is lightweight and functional.",
        "d": "Easy"
    },
    {
        "q": "How do you prevent 'Cascading Failures' in microservices?",
        "a": "Use timeouts on all external calls, implement circuit breakers, use bulkhead pattern (isolate thread pools), and have sensible fallbacks for every dependency.",
        "d": "Medium"
    },
    {
        "q": "Explain 'Serverless' in the context of Spring Boot. What is Spring Cloud Function?",
        "a": "It allows writing logic as simple Java Functions (java.util.function.Function). Spring Cloud Function then adapts these to run on AWS Lambda, Azure Functions, or Google Cloud Functions without changing the code.",
        "d": "Medium"
    },
    {
        "q": "How do you implement 'Multi-Region Failover' for a Spring Boot application on AWS?",
        "a": "Deploy the app in two regions. Use Route 53 with 'Health Checks' and 'Failover Routing'. If Region A goes down, Route 53 automatically directs traffic to Region B.",
        "d": "Hard"
    },
    {
        "q": "What is 'Chaos Engineering' (e.g., Chaos Monkey) and how does it help microservices?",
        "a": "Intentionally injecting failures (killing pods, adding latency) into production to ensure the system is resilient. If the system stays up during chaos, you have high confidence in its reliability.",
        "d": "Medium"
    },
    {
        "q": "Describe the 'Ambassador Pattern'.",
        "a": "A helper container that handles common tasks like logging, monitoring, and security for a primary application. Similar to sidecar but focuses on outgoing connections.",
        "d": "Hard"
    },
    {
        "q": "How do you handle 'Security Tokens' (JWT) in a logout scenario if the tokens are stateless?",
        "a": "You can't 'delete' a stateless token. You must implement a 'Blacklist' in a fast store like Redis. Store the token ID until its original expiry time; check the blacklist on every request.",
        "d": "Medium"
    },
    {
        "q": "Explain 'Graceful Degradation'. Give an example.",
        "a": "If a non-essential service fails, the system stays up with limited features. Example: If the 'Recommendations' service is down, the E-commerce site still allows buying products but just hides the 'You may also like' section.",
        "d": "Easy"
    }
]

# --- MESSAGING (40) ---
messaging_scenarios = [
    {
        "q": "You need to ensure that messages in Kafka are processed in the exact order they were sent. How do you configure this?",
        "a": "Use the same 'Partition Key' for related messages. Kafka guarantees ordering within a single partition. Also, set 'max.in.flight.requests.per.connection=1' to prevent reordering during retries.",
        "d": "Medium"
    },
    {
        "q": "Explain the difference between 'At-most-once', 'At-least-once', and 'Exactly-once' delivery in messaging.",
        "a": "At-most-once: No retries, message might be lost. At-least-once: Retries on failure, might get duplicates (most common). Exactly-once: Complex, requires transaction support in both broker and consumer to ensure effect happens once.",
        "d": "Medium"
    },
    {
        "q": "Your Kafka consumer is too slow, and 'Consumer Lag' is increasing. How do you scale it up?",
        "a": "Increase the number of partitions in the topic and then increase the number of consumer instances in the same Consumer Group (up to the number of partitions).",
        "d": "Easy"
    },
    {
        "q": "How do you implement a 'Dead Letter Queue' (DLQ) in RabbitMQ using Spring AMQP?",
        "a": "Configure an 'x-dead-letter-exchange' and 'x-dead-letter-routing-key' on your primary queue. If a message is rejected with 'requeue=false', it automatically moves to the DLQ.",
        "d": "Medium"
    },
    {
        "q": "What is the 'Transactional Outbox Pattern'? Why is it used when sending messages to Kafka from a database-backed service?",
        "a": "It ensures atomicity between DB update and message sending. Instead of sending to Kafka directly, save the message in an 'OUTBOX' table in the same DB transaction. A separate process then reads the table and sends to Kafka.",
        "d": "Hard"
    },
    {
        "q": "How do you handle 'Large Messages' (e.g., 50MB files) in Kafka, given its default limit is 1MB?",
        "a": "Don't send the file. Store it in S3 and send the S3 URL in the Kafka message (Claim Check Pattern). If you MUST send it, increase 'max.request.size' on producer and 'message.max.bytes' on broker.",
        "d": "Medium"
    },
    {
        "q": "Explain 'Consumer Groups' in Kafka. What happens if you have more consumers than partitions?",
        "a": "Consumer Groups allow load balancing. Each partition is assigned to exactly one consumer in the group. If consumers > partitions, the extra consumers remain idle and act as hot-standbys.",
        "d": "Easy"
    },
    {
        "q": "How do you implement 'Message Retries' with Exponential Backoff in a Spring Boot Kafka consumer?",
        "a": "Use 'DefaultErrorHandler' or 'SeekToCurrentErrorHandler'. Configure a 'BackOff' bean (e.g., ExponentialBackOff with initial interval 1s, multiplier 2.0).",
        "d": "Medium"
    },
    {
        "q": "What is 'Compacted Topic' in Kafka? Give a real-world use case.",
        "a": "A topic that only keeps the latest value for each key. Perfect for storing 'current state' (e.g., current user addresses or product prices), where you don't care about the history of changes.",
        "d": "Medium"
    },
    {
        "q": "Explain the difference between 'Fanout', 'Direct', and 'Topic' exchanges in RabbitMQ.",
        "a": "Fanout: Broadcasts to all bound queues. Direct: Routes to queue with exact matching routing key. Topic: Routes based on wildcard matching (e.g., 'logs.*', 'logs.#').",
        "d": "Easy"
    },
    {
        "q": "How do you implement 'Request-Response' pattern over a message broker in Spring Boot?",
        "a": "Use Spring's 'ReplyingKafkaTemplate' or 'RabbitTemplate.sendAndReceive'. It generates a 'Correlation ID' and waits for a response on a temporary 'reply' queue.",
        "d": "Hard"
    },
    {
        "q": "Your Kafka broker goes down. How does the 'Acks' setting on the producer affect data durability?",
        "a": "acks=0: No confirmation (fast, risky). acks=1: Leader confirmed (safe unless leader dies before replication). acks=all: All replicas confirmed (slowest, most durable).",
        "d": "Medium"
    },
    {
        "q": "What is 'Backpressure' in a messaging system? How is it handled in Spring WebFlux + Kafka?",
        "a": "Backpressure happens when the producer sends faster than the consumer can process. In WebFlux, the consumer 'requests' only N items, and the Kafka driver pauses fetching until the consumer is ready for more.",
        "d": "Hard"
    },
    {
        "q": "Explain 'Zookeeper's' role in older Kafka versions vs its removal in KRaft mode.",
        "a": "Older versions used Zookeeper for cluster metadata and leader election. KRaft (Kafka Raft) moves this metadata into an internal Kafka topic, removing the external Zookeeper dependency and improving scalability.",
        "d": "Medium"
    },
    {
        "q": "How do you handle 'Schema Evolution' in Kafka messages (e.g., adding a field to a JSON message)?",
        "a": "Use Avro or Protobuf with a 'Schema Registry'. This ensures that producers and consumers always agree on the message format and allows for backward/forward compatibility checks.",
        "d": "Hard"
    },
    {
        "q": "What is 'Idempotent Producer' in Kafka? How do you enable it?",
        "a": "It prevents duplicate messages caused by producer retries (e.g., network error after successful write). Enable by setting 'enable.idempotence=true'. It uses a sequence number for every message.",
        "d": "Medium"
    },
    {
        "q": "How do you implement 'Message TTL' (Time To Live) in RabbitMQ?",
        "a": "Set the 'x-message-ttl' argument when declaring the queue, or set the 'expiration' property on an individual message. Expired messages are moved to the DLQ or discarded.",
        "d": "Easy"
    },
    {
        "q": "Explain 'Exclusive Consumer' in RabbitMQ. When is it used?",
        "a": "Ensures that only one consumer can read from a queue. Useful when you need strict global ordering across the entire queue, but it limits scalability.",
        "d": "Medium"
    },
    {
        "q": "How do you handle 'Poison Pill' messages (messages that always cause the consumer to crash)?",
        "a": "Catch exceptions in the consumer, log the error, and send the message to a DLQ manually. Don't let it requeue indefinitely, or it will block the entire partition/queue.",
        "d": "Medium"
    },
    {
        "q": "Explain 'Kafka Streams' vs 'Spark Streaming'.",
        "a": "Kafka Streams is a lightweight Java library that runs within your Spring app (no cluster needed). Spark Streaming is a heavy distributed processing engine that requires its own cluster. Use Kafka Streams for simple transformations/joins.",
        "d": "Medium"
    },
    {
        "q": "What is 'Long Polling' in the context of a message consumer?",
        "a": "The consumer asks the broker for messages and the broker holds the request open until a message arrives (or a timeout occurs). This reduces network overhead compared to frequent short polling.",
        "d": "Easy"
    },
    {
        "q": "How do you implement 'Priority Queues' in RabbitMQ?",
        "a": "Set 'x-max-priority' when creating the queue. When sending, set the 'priority' property on the message. RabbitMQ will deliver higher priority messages first.",
        "d": "Medium"
    },
    {
        "q": "Explain 'Rebalance' in Kafka. Why should it be avoided if possible?",
        "a": "Rebalance happens when a consumer joins/leaves a group, causing partitions to be reassigned. It stops all processing (Stop the World) for the group. Avoid by tuning 'session.timeout.ms' and 'max.poll.interval.ms'.",
        "d": "Hard"
    },
    {
        "q": "How do you secure Kafka communication using SSL/TLS in Spring Boot?",
        "a": "Configure 'security.protocol=SSL', 'ssl.truststore.location', and 'ssl.keystore.location' in the Spring properties. The producer and consumer will then encrypt all traffic to the broker.",
        "d": "Medium"
    },
    {
        "q": "What is 'MirrorMaker' in Kafka?",
        "a": "A tool used to replicate data between two Kafka clusters (e.g., between two data centers for Disaster Recovery).",
        "d": "Easy"
    },
    {
        "q": "Explain 'Message Prefetch' (QoS) in RabbitMQ. Why is setting it to 1 sometimes necessary?",
        "a": "Prefetch limits how many unacknowledged messages a consumer can have. Setting it to 1 ensures that a fast consumer doesn't 'hog' messages while a slow one sits idle, enabling better load balancing.",
        "d": "Medium"
    },
    {
        "q": "How do you implement 'Delayed Delivery' (Scheduled Messaging) in Kafka?",
        "a": "Kafka doesn't support this natively. You must either use a separate topic for 'future' messages and a process that polls and moves them, or use a tool like 'Kafka Delayed Message Exchange' (non-standard).",
        "d": "Hard"
    },
    {
        "q": "What are 'Headers' in Kafka messages? Give a use case.",
        "a": "Key-value pairs sent alongside the payload. Use case: Storing 'traceId' for distributed tracing, 'contentType' for serialization, or 'appVersion' to handle different processing logic.",
        "d": "Easy"
    },
    {
        "q": "Explain 'Batching' in Kafka producers. How do 'linger.ms' and 'batch.size' interact?",
        "a": "The producer waits up to 'linger.ms' to see if more messages arrive to fill a 'batch.size' buffer. This increases throughput by sending fewer, larger network requests at the cost of slight latency.",
        "d": "Medium"
    },
    {
        "q": "How do you handle 'Consumer Offset Management' in Spring Kafka? Manual vs Automatic.",
        "a": "Automatic: Kafka commits offsets every few seconds (risk of duplicates). Manual: You call 'acknowledgment.acknowledge()' after processing. Manual is safer for 'At-least-once' delivery guarantees.",
        "d": "Medium"
    },
    {
        "q": "What is 'Persistent' vs 'Transient' messages in RabbitMQ?",
        "a": "Persistent messages are written to disk and survive a broker restart (if the queue is also durable). Transient messages are memory-only and lost on restart. Use Persistent for critical data.",
        "d": "Easy"
    },
    {
        "q": "Explain 'Reliable Delivery' in RabbitMQ. What are 'Publisher Confirms' and 'Consumer Acks'?",
        "a": "Publisher Confirms: The broker tells the producer 'I got it'. Consumer Acks: The consumer tells the broker 'I finished it'. Both are needed for end-to-end reliability.",
        "d": "Medium"
    },
    {
        "q": "How do you implement 'Content-Based Routing' with RabbitMQ?",
        "a": "Use a 'Topic Exchange'. The producer sets a routing key like 'order.created.electronics'. Consumers bind queues with patterns like 'order.created.*' or '#.electronics'.",
        "d": "Easy"
    },
    {
        "q": "What is 'Log Segments' in Kafka? How does retention policy work?",
        "a": "Kafka stores partitions in 'segments' (files). When a segment reaches a certain age or size, it's closed and eventually deleted based on 'retention.ms' or 'retention.bytes'.",
        "d": "Medium"
    },
    {
        "q": "Explain 'In-Sync Replicas' (ISR) in Kafka.",
        "a": "The set of replicas that are currently caught up with the leader. If the leader fails, only a member of the ISR can be elected as the new leader (unless 'unclean.leader.election' is true).",
        "d": "Medium"
    },
    {
        "q": "How do you perform 'Unit Testing' for a Kafka Consumer in Spring Boot without a real Kafka broker?",
        "a": "Use '@EmbeddedKafka'. it starts an in-memory Kafka broker during the test. Alternatively, use 'MockConsumer' to verify logic without any broker at all.",
        "d": "Medium"
    },
    {
        "q": "What is 'Pulsar' and how does it compare to Kafka for a Spring Boot developer?",
        "a": "Pulsar is a newer messaging system that separates storage from serving, allowing independent scaling. It supports both queuing (like RabbitMQ) and streaming (like Kafka) natively.",
        "d": "Hard"
    },
    {
        "q": "How do you implement 'Multi-Tenancy' in a Kafka topic?",
        "a": "Commonly done by prefixing topic names (tenant1.orders, tenant2.orders) or using a 'tenantId' header in every message and filtering in the consumer.",
        "d": "Hard"
    },
    {
        "q": "Explain 'Message Deduplication' on the consumer side.",
        "a": "Since 'Exactly-once' is hard, consumers should be idempotent. Store the ID of processed messages in a DB/Redis with a TTL. If an ID is seen again, skip processing.",
        "d": "Medium"
    },
    {
        "q": "What is 'Replayability' in Kafka and why is it useful?",
        "a": "Because Kafka persists messages for a duration, a new consumer can start from 'offset 0' and 'replay' the entire history. Useful for recovering from bugs or populating a new search index.",
        "d": "Easy"
    }
]

# --- TESTING & PERFORMANCE (40) ---
performance_scenarios = [
    {
        "q": "Your Spring Boot app starts up very slowly (2 minutes). How do you diagnose which bean is taking the most time?",
        "a": "Use 'spring-boot-starter-actuator' and look at the '/actuator/startup' endpoint (Spring Boot 2.4+). It provides a JSON tree of every bean's initialization time.",
        "d": "Medium"
    },
    {
        "q": "Explain 'Virtual Threads' (Project Loom) in Java 21. How do they improve Spring Boot performance for I/O bound apps?",
        "a": "They are lightweight threads managed by the JVM, not the OS. They allow running millions of threads. In Spring Boot 3.2+, you can enable them with 'spring.threads.virtual.enabled=true', significantly increasing throughput for blocked I/O.",
        "d": "Hard"
    },
    {
        "q": "How do you implement 'Caching' in Spring Boot to avoid hitting the database for static data like 'Product Categories'?",
        "a": "Use '@EnableCaching' and annotate the service method with '@Cacheable(\"categories\")'. Configure a provider like Caffeine (local) or Redis (distributed).",
        "d": "Easy"
    },
    {
        "q": "What is 'Spring Boot Actuator'? List 3 endpoints useful for performance monitoring.",
        "a": "Actuator provides production-ready features. '/metrics' (JVM, CPU), '/heapdump' (for memory leaks), and '/prometheus' (for monitoring with Grafana).",
        "d": "Easy"
    },
    {
        "q": "How do you perform 'Load Testing' on a Spring Boot REST API? Which tools would you use?",
        "a": "Tools: JMeter, Gatling, or k6. Create a script that simulates 1000 concurrent users and measure response time, throughput (RPS), and error rate.",
        "d": "Easy"
    },
    {
        "q": "Your application has a memory leak. How do you find the root cause using a Heap Dump?",
        "a": "Capture dump via 'jmap' or Actuator. Open it in Eclipse MAT. Look for the 'Leak Suspects' report to see which objects are occupying the most memory and which classes are holding references to them.",
        "d": "Medium"
    },
    {
        "q": "Explain 'L1 vs L2 Cache' in the context of Spring Boot applications.",
        "a": "L1: Hibernate's session-level cache (per request). L2: Shared cache across all sessions (Ehcache/Redis). L1 is automatic; L2 requires explicit configuration and is used for read-heavy data.",
        "d": "Medium"
    },
    {
        "q": "How do you optimize 'JSON Serialization' performance if you have massive payloads?",
        "a": "Use Jackson's 'Afterburner' or 'Blackbird' module. Alternatively, use a faster binary format like Protobuf or Avro instead of JSON for internal service communication.",
        "d": "Hard"
    },
    {
        "q": "What is 'JIT Compilation' and how does 'Warm-up' affect Spring Boot performance in a container?",
        "a": "JIT compiles bytecode to machine code at runtime for hot spots. In K8s, a new pod is 'cold' and slow. Use 'Pre-warming' (sending fake requests) or AppCDS to speed up the initial performance.",
        "d": "Hard"
    },
    {
        "q": "How do you implement 'Connection Pooling' for your database in Spring Boot? Why is it necessary?",
        "a": "Spring Boot uses HikariCP by default. It's necessary because creating a new DB connection for every request is extremely slow and resource-intensive. Pooling reuses existing connections.",
        "d": "Easy"
    },
    {
        "q": "Your API response time is high. How do you use 'Spring AOP' to log the execution time of all methods in a specific package?",
        "a": "Create an @Around aspect. Capture 'System.currentTimeMillis()' before and after 'joinPoint.proceed()', then log the difference along with the method name.",
        "d": "Medium"
    },
    {
        "q": "Explain the difference between '@SpringBootTest' and '@WebMvcTest'. When would you use each?",
        "a": "@SpringBootTest starts the full application context (slow, integration test). @WebMvcTest starts only the web layer (MockMvc, fast, unit test for controllers).",
        "d": "Easy"
    },
    {
        "q": "How do you use 'Testcontainers' to test your JPA repositories with a real PostgreSQL database instead of H2?",
        "a": "In your test, use '@Container' to start a PostgreSQLContainer. Use '@DynamicPropertySource' to inject the container's random port and credentials into the Spring environment.",
        "d": "Medium"
    },
    {
        "q": "What is 'MockMvc' and how do you use it to test a secured endpoint?",
        "a": "A tool to perform requests against the DispatcherServlet without a real server. Use 'with(user(\"admin\").roles(\"ADMIN\"))' to simulate an authenticated user in the test.",
        "d": "Easy"
    },
    {
        "q": "How do you test 'Asynchronous Methods' (@Async) in Spring Boot?",
        "a": "Use Awaitility library. It allows you to 'waitAtMost(5, SECONDS).until(() -> resultIsReady())'. You cannot use standard assertions because the method returns immediately.",
        "d": "Medium"
    },
    {
        "q": "Explain 'Property-Based Testing' (e.g., using jqwik). How is it different from traditional unit tests?",
        "a": "Traditional tests use specific inputs. Property-based tests generate 1000s of random inputs to verify a 'property' (e.g., 'sorting an array shouldn't change its size'). Great for finding edge cases.",
        "d": "Hard"
    },
    {
        "q": "How do you implement 'Database Mocking' for service layer tests using Mockito?",
        "a": "Annotate the service with '@InjectMocks' and the repository with '@Mock'. Use 'when(repo.findById(1L)).thenReturn(Optional.of(entity))' to define mock behavior.",
        "d": "Easy"
    },
    {
        "q": "What is 'Mutation Testing' (e.g., PITest) and why is it better than simple Code Coverage?",
        "a": "Mutation testing modifies your code (e.g., changes '>' to '<') and checks if your tests fail. If they don't, your tests aren't actually verifying the logic, even if coverage is 100%.",
        "d": "Hard"
    },
    {
        "q": "How do you profile a Spring Boot application running in production without stopping it?",
        "a": "Use 'Java Flight Recorder' (JFR). You can start a recording via 'jcmd', let it run for 10 minutes, and then analyze the '.jfr' file in JDK Mission Control.",
        "d": "Medium"
    },
    {
        "q": "Explain 'G1 GC' vs 'ZGC' for Spring Boot applications. Which one is better for low latency?",
        "a": "G1 is the default and balances throughput/latency. ZGC (available in Java 15+) is designed for sub-millisecond pause times regardless of heap size. Use ZGC for ultra-low latency requirements.",
        "d": "Hard"
    },
    {
        "q": "How do you optimize 'Docker Image Size' for a Spring Boot app?",
        "a": "Use 'Multi-stage builds'. Compile in one stage, and in the second stage, use a minimal JRE image (like Alpine or Distroless) and copy only the final jar.",
        "d": "Medium"
    },
    {
        "q": "What is 'Layered Jar' in Spring Boot and how does it improve Docker build speed?",
        "a": "It splits the jar into layers (dependencies, spring-boot, application). Since dependencies rarely change, Docker can cache that layer, making subsequent builds/pushes much faster.",
        "d": "Medium"
    },
    {
        "q": "How do you implement 'Throttling' in a Spring Boot application using Resilience4j?",
        "a": "Use '@RateLimiter(name = \"myApi\")'. Configure 'limitForPeriod' and 'limitRefreshPeriod' in application.yml. Useful for protecting your own resources from abuse.",
        "d": "Easy"
    },
    {
        "q": "Explain 'Bulkhead Pattern' for performance isolation.",
        "a": "It isolates resources (like thread pools) for different parts of the system. If the 'Payment' thread pool is full, it doesn't prevent the 'Search' feature from working. Prevents a single slow component from consuming all system threads.",
        "d": "Medium"
    },
    {
        "q": "Your database queries are slow. How do you find the 'Slowest Queries' in a Spring Boot app?",
        "a": "Enable Hibernate's slow query logging or use a database-specific tool (like PG_STAT_STATEMENTS). In Spring, you can use a ProxyDataSource to log any query taking longer than X ms.",
        "d": "Easy"
    },
    {
        "q": "How do you implement 'Compression' (GZIP) for your Spring Boot REST responses?",
        "a": "Set 'server.compression.enabled=true' and 'server.compression.mime-types=application/json,text/html,...'. This reduces payload size significantly at the cost of slight CPU usage.",
        "d": "Easy"
    },
    {
        "q": "What is 'Native Image' (GraalVM) and how does it affect Spring Boot startup time?",
        "a": "It compiles the Java app to a native binary ahead-of-time. Startup time drops from seconds to milliseconds and memory usage is significantly lower. Perfect for Serverless/Lambda.",
        "d": "Hard"
    },
    {
        "q": "Explain 'Context Propagation' in a reactive (WebFlux) application.",
        "a": "Since reactive code jumps between threads, ThreadLocal doesn't work. You must use 'Context' (similar to a map) that is passed along the reactive stream. Essential for security and tracing.",
        "d": "Hard"
    },
    {
        "q": "How do you test 'Global Exception Handling' (@ControllerAdvice) using MockMvc?",
        "a": "Perform a request that you know will trigger an exception (e.g., GET /user/999 for a missing user). Verify that the status code and JSON body match your custom error format.",
        "d": "Easy"
    },
    {
        "q": "What is 'WireMock' and how do you use it for integration testing?",
        "a": "A tool to mock external HTTP APIs. You start a WireMock server and tell it to return '200 OK' with a specific JSON when a specific URL is called, allowing you to test your 'Feign Client' logic.",
        "d": "Medium"
    },
    {
        "q": "How do you handle 'Resource Cleanup' in integration tests (e.g., deleting data from a shared DB)?",
        "a": "Use '@Transactional' on the test method. Spring will automatically roll back the transaction after the test finished, leaving the DB clean. For non-DB resources, use @AfterEach.",
        "d": "Easy"
    },
    {
        "q": "Explain the '@SpyBean' annotation in Spring Boot tests.",
        "a": "It creates a 'spy' around a real Spring bean. You can mock specific methods while keeping the rest of the bean's real behavior. Use sparingly as it can lead to fragile tests.",
        "d": "Medium"
    },
    {
        "q": "How do you use 'Spring Boot DevTools' to speed up development?",
        "a": "It provides 'LiveReload' (automatic browser refresh) and 'Restart' (fast app restart when code changes). It also disables template caching so you see UI changes immediately.",
        "d": "Easy"
    },
    {
        "q": "Explain 'Pre-Stop Hook' in a Kubernetes pod for Spring Boot.",
        "a": "A command executed before the container is terminated. Use it to call 'curl -X POST /actuator/shutdown' or to sleep for 20s to give the Load Balancer time to stop sending traffic.",
        "d": "Hard"
    },
    {
        "q": "How do you measure 'Code Coverage' in a Spring Boot project using Maven?",
        "a": "Add the 'jacoco-maven-plugin'. Run 'mvn test'. It generates an HTML report showing exactly which lines of code were executed by your tests.",
        "d": "Easy"
    },
    {
        "q": "What is 'Contract First' vs 'Code First' API development?",
        "a": "Contract First: Write OpenAPI (Swagger) spec first, then generate Java code. Code First: Write Java code with annotations, then generate Swagger spec. Contract First is better for team collaboration.",
        "d": "Medium"
    },
    {
        "q": "How do you implement 'Database Indexing' strategy for a high-traffic Spring Boot app?",
        "a": "Identify slow queries via logs. Add indexes to columns used in WHERE, JOIN, and ORDER BY clauses. Be careful: too many indexes slow down INSERT/UPDATE operations.",
        "d": "Easy"
    },
    {
        "q": "Explain 'Backpressure' in the context of Project Reactor (Mono/Flux).",
        "a": "It's a mechanism where a consumer signals to a producer how much data it can handle. This prevents the producer from overwhelming the consumer with more data than it can process.",
        "d": "Medium"
    },
    {
        "q": "How do you implement 'API Documentation' in Spring Boot using Springdoc-openapi?",
        "a": "Add the dependency. It automatically scans your controllers and generates a UI at '/swagger-ui.html'. Use @Operation and @ApiResponse annotations to add detail.",
        "d": "Easy"
    },
    {
        "q": "Explain 'Thread Dump' analysis. When would you need one?",
        "a": "A snapshot of all active threads. You need one when your app is 'hung' or experiencing a 'Deadlock'. It shows exactly what each thread is doing and which locks it's holding.",
        "d": "Medium"
    }
]

# Combine all categories
all_scenarios = security_scenarios + persistence_scenarios + microservice_scenarios + messaging_scenarios + performance_scenarios

# Final check for length
if len(all_scenarios) != 200:
    print(f"Warning: Count is {len(all_scenarios)}")

# Convert to final format
final_json = []
for i, item in enumerate(all_scenarios):
    final_json.append({
        "topic": "Spring Boot",
        "question": item["q"],
        "answer": item["a"],
        "difficulty": item["d"]
    })

print(json.dumps(final_json, indent=2))
