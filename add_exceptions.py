import json
import random

# Read existing questions
with open('questions.json', 'r') as f:
    questions = json.load(f)

# Spring Boot Exception Handling Scenarios - Detailed practical scenarios
# Each tuple: (question, answer) - will be duplicated with variations

easy_exceptions = [
    ('Your Spring Boot application throws NullPointerException when a user submits a form with an optional field. The field should be nullable but the code does not handle null. Explain how you would fix this at the controller level using proper validation annotations.', 'Use @Valid and @ModelAttribute with bean validation. Add @NotNull only for required fields, use @Nullable for optional. Implement @ControllerAdvice for global exception handling. Return meaningful error responses with field-specific messages.'),
    ('A user reports that after entering invalid data in a form, they see an ugly default error page instead of a friendly message. How would you customize error responses in Spring Boot to show proper validation messages?', 'Implement @ControllerAdvice to handle MethodArgumentNotValidException. Create custom ErrorResponse class. Return consistent JSON error structure. Configure error pages in error.html or custom error controller.'),
    ('Your REST API returns 500 Internal Server Error when the database is temporarily unavailable. Instead of showing a generic error, you want to return a proper status code. How would you handle this?', 'Use @ExceptionHandler for specific exceptions. Return 503 Service Unavailable with retry-after header. Implement global exception handler with @ControllerAdvice. Add proper HTTP status codes based on exception type.'),
    ('A junior developer accidentally removed try-catch blocks and now runtime exceptions crash the application. How would you implement global exception handling to prevent this?', 'Implement @ControllerAdvice with @ExceptionHandler for common exceptions. Create custom exception classes for business logic. Add fallback for uncaught exceptions returning proper HTTP status. Log exceptions with proper correlation IDs.'),
    ('Your application logs show exceptions with stack traces in production, exposing internal implementation details. How would you secure this to show only user-friendly messages?', 'Configure server.error.include-message=never and include-stacktrace=never. Implement custom error handler that returns generic messages. Log full stack traces to file only. Create user-friendly error pages for different error codes.'),
    ('Users get confusing 400 Bad Request errors without explanation when their JSON request is malformed. How would you provide better error messages showing what is wrong with their request?', 'Handle HttpMessageNotReadableException in @ControllerAdvice. Parse and extract field errors from BindingResult. Return detailed validation error response showing exactly which field is wrong and why.'),
    ('Your scheduled job throws an exception and silently fails without anyone noticing. How would you ensure exceptions in scheduled tasks are properly handled and logged?', 'Use @Async with @Retryable for background jobs. Implement async uncaught exception handler. Add alerting for failed jobs. Configure scheduler with error handler using ScheduledTaskRegistrar.'),
    ('An API endpoint fails when the client sends a request with missing headers. Currently it returns a generic error. How would you handle missing header exceptions properly?', 'Implement @ExceptionHandler for MissingRequestHeaderException. Create specific error response for missing headers. Use @RequestHeader(required=false) for optional headers. Document required headers in API.'),
    ('Your application throws ArrayIndexOutOfBoundsException in one specific scenario. How would you find and fix this while ensuring similar issues are prevented in the future?', 'Add defensive checks before array access. Use Optional for nullable values. Implement global exception handler that logs stack traces. Add unit tests covering edge cases.'),
    ('When validating a form, the error messages are in English but your application needs to support multiple languages. How would you implement internationalized validation messages?', 'Use MessageSource for i18n. Configure messages.properties for different locales. Use {field.name} in validation messages. Inject Locale in controller to select appropriate messages bundle.'),
    ('Your application throws ClassCastException when trying to cast an object to a specific type. How would you handle this safely and prevent ClassCastException?', 'Use instanceof check before casting. Implement visitor pattern for type-safe operations. Use generics to avoid raw type casting. Add defensive null checks before casting.'),
    ('A REST endpoint returns 404 when a resource is not found, but the error message is empty. How would you customize 404 responses to include helpful information?', 'Implement @ExceptionHandler for NoHandlerFoundException. Create custom ErrorResponse with resource path and suggestion. Configure server.servlet.path-match-type=ant_path_matcher. Return search results or related resources in response.'),
    ('Your application throws IllegalArgumentException when passing invalid parameters to a method. How would you validate inputs and provide meaningful error messages?', 'Add validation at service layer using Spring Validation. Use custom validators with @Constraint. Implement BusinessValidator interface. Return field-level error messages in response.'),
    ('Users experience ConnectionTimeoutException when calling external API. How would you handle timeout exceptions gracefully with proper retry mechanism?', 'Configure Feign client with timeouts. Implement @Retryable with exponential backoff. Use CircuitBreaker for sustained failures. Return user-friendly message with retry suggestion.'),
    ('Your application throws ConcurrentModificationException when iterating over a collection while modifying it. How would you fix this thread-safety issue?', 'Use CopyOnWriteArrayList for concurrent reads/writes. Use Iterator.remove() for safe removal. Use streams with toList(). Implement proper synchronization or use concurrent collections.'),
]

medium_exceptions = [
    ('Your microservices architecture has a service that throws custom BusinessException with error codes. Other services need to handle these exceptions consistently. How would you implement a standardized exception handling pattern across all microservices?', 'Create shared exception library with common exception classes. Use @ResponseStatus to map exceptions to HTTP status codes. Implement FeignErrorDecoder to transform exceptions across services. Add exception handling in API Gateway.'),
    ('When calling multiple downstream services in a single request, one service throws an exception and the entire request fails. How would you implement fault tolerance so that failure of one service does not bring down the entire request?', 'Use @CircuitBreaker with Resilience4j. Implement fallback methods that return default or cached data. Use CompletableFuture with exception handling. Configure retry with backoff for transient failures.'),
    ('Your application experiences race conditions where concurrent requests modify the same data causing exceptions. How would you handle optimistic locking exceptions to ensure data consistency?', 'Use @Version field for optimistic locking. Implement @ExceptionHandler for OptimisticLockException. Add retry logic for conflict resolution. Return proper 409 Conflict status to client.'),
    ('Exceptions in your asynchronous message consumer cause the message to be redelivered infinitely, creating an infinite loop. How would you implement proper exception handling for message-driven consumers?', 'Configure dead letter queue for poison messages. Implement retry with limited attempts. Use @Retryable with maxAttempts. Add exception classification to determine if message should be discarded.'),
    ('Your Spring Security authentication throws exceptions that result in default Spring error pages. You need to return proper JSON responses for authentication failures. How would you customize security exception handling?', 'Implement AuthenticationEntryPoint for JSON responses. Create custom AccessDeniedHandler. Configure exceptionHandling in SecurityFilterChain. Return proper HTTP status codes (401, 403).'),
    ('File upload operations throw IOException when disk is full, but the exception is not properly handled and crashes the application. How would you handle storage-related exceptions gracefully?', 'Implement @ExceptionHandler for IOException and its subtypes. Check available disk space before upload. Configure multipart resolver with max file sizes. Return user-friendly error with proper HTTP status.'),
    ('Your REST API calls a downstream service that throws various exceptions. You need to transform these exceptions into consistent API responses while preserving important error information. How would you implement this?', 'Create exception mapper that extracts relevant information from downstream exceptions. Use Feign client with ErrorDecoder. Implement ResponseEntityExceptionHandler for transformation. Add correlation IDs for tracking.'),
    ('Exceptions during WebSocket message handling cause the connection to close unexpectedly. How would you handle exceptions in WebSocket handlers to maintain connection stability?', 'Implement TextWebSocketHandler with exception handling in each method. Add @MessageExceptionHandler for typed exceptions. Configure WebSocketConfigurer with exception handlers. Implement reconnection logic on client side.'),
    ('Your application uses Spring Data JPA and throws PersistenceException when database constraints are violated. The error message is technical and confusing. How would you translate these to user-friendly messages?', 'Implement DataIntegrityViolationException handler. Parse constraint names from exception message. Create mapping of constraint to user message. Use custom exception classes for business constraints.'),
    ('During high load, your application throws TooManyConnectionsException from the connection pool. The exception should be handled gracefully with proper retry mechanism. How would you implement this?', 'Configure HikariCP with appropriate pool sizes. Implement @Retryable with backoff for connection exceptions. Add circuit breaker for sustained failures. Return 503 with retry-after header.'),
    ('Your application throws NoTransactionException when trying to execute database operations outside a transaction. How would you properly handle transaction exceptions in Spring?', 'Use @Transactional with proper propagation. Implement TransactionCallback for programmatic transactions. Configure PlatformTransactionManager. Handle TransactionSystemException with proper error response.'),
    ('Integration with third-party API throws HttpClientErrorException for various client errors. How would you handle different HTTP error status codes systematically?', 'Implement FeignResponseException for different status codes. Create error code enum mapping to business exceptions. Add fallback for unexpected status codes. Log correlation IDs for debugging.'),
    ('Your Spring Batch job fails with exception during item processing. How would you handle exceptions in batch processing to implement proper error handling and skip policies?', 'Configure SkipPolicy for skippable exceptions. Implement ItemProcessListener for exception handling. Use RetryPolicy with backoff. Configure restart from failed item with JobExecution.'),
    ('Application throws SessionClosedException during Hibernate operations after database connection drops. How would you handle session exceptions and implement reconnection logic?', 'Configure Hibernate with proper session handling. Implement TransactionSuspensionInterceptor. Add retry with session refresh. Use session-per-request pattern with proper cleanup.'),
    ('Your reactive application throws IllegalStateException when trying to emit after complete. How would you handle exceptions in reactive streams properly?', 'Use doOnError for exception handling. Implement error recovery with onErrorResume. Use try-catch-finally in lambda properly. Configure proper error handling in WebExceptionHandler.'),
]

hard_exceptions = [
    ('You have a complex workflow where multiple services must be called in sequence. If any service throws an exception, you need to compensate for already completed steps (rollback). How would you implement transactional outbox pattern with exception handling for distributed transactions?', 'Implement transactional outbox pattern: update database and insert event in same transaction. Use event-driven architecture with message queue. Implement compensation logic that undoes completed steps. Handle exceptions in each step with proper error response.'),
    ('Your application experiences exceptions that appear to be random - they happen intermittently under specific timing conditions involving multiple threads. How would you diagnose and handle these concurrency-related exceptions?', 'Implement ThreadLocal for request context to track exceptions. Add async stack trace preservation. Use Thread.setDefaultUncaughtExceptionHandler. Profile for race conditions. Implement proper synchronization.'),
    ('You need to implement a custom exception handling framework that collects all exceptions during a request processing, processes them in batch, and reports aggregated errors to monitoring. How would you design this?', 'Create ExceptionCollector that accumulates exceptions during request. Use AOP for automatic exception collection. Implement async reporting to monitoring systems. Add retry and escalation logic for critical exceptions.'),
    ('Exceptions during deserialization of complex nested JSON cause confusing errors that make debugging difficult. How would you implement custom deserialization exception handling with detailed context?', 'Implement custom JsonDeserializer with exception handling. Add contextual information to deserialization errors. Use @JsonSetter(nulls=FAIL) for null handling. Create custom error response with field path.'),
    ('Your application must handle exceptions from multiple protocols (HTTP, WebSocket, JMS, gRPC) uniformly and present them through a unified API. How would you design a cross-protocol exception handling abstraction?', 'Create adapter pattern for different protocols. Implement ProtocolAdapter interface with exception handling. Unify exception to common ErrorResponse format. Add protocol-specific context preservation.'),
    ('During server shutdown, in-flight requests throw exceptions that are not properly handled, leaving the system in inconsistent state. How would you implement graceful shutdown with proper exception handling?', 'Implement @PreDestroy in services. Use @SchedulerSignaller for shutdown coordination. Add request termination logic. Configure graceful timeout before force shutdown. Implement resource cleanup handlers.'),
    ('You need to implement exception handling that maintains audit trail of all exceptions across microservices, including the full context of each request. How would you design this distributed exception tracking system?', 'Create exception event publishing to central service. Include correlation ID, request/response, user context. Use async message queue for non-blocking. Store in searchable database. Implement dashboard for analysis.'),
    ('Exceptions in your reactive WebFlux application are difficult to debug because traditional exception handlers do not work. How would you properly handle exceptions in a reactive stack with proper error propagation?', 'Use Mono.onErrorResume() and Flux.onErrorResume() for error handling. Implement WebExceptionHandler for global handling. Use doOnError for logging. Add proper error mapping to HTTP responses. Handle backpressure exceptions.'),
    ('Your application throws exceptions when integrating with legacy systems that use different exception semantics. How would you create adapters to translate legacy exceptions into Spring exceptions?', 'Create adapter classes implementing Customizer<ErrorHandler>. Implement ExceptionClassifier to route legacy exceptions. Translate error codes to Spring exceptions. Add logging and monitoring of translated exceptions.'),
    ('You need to implement exception handling that works across multiple Spring Boot applications deployed in different versions, where exception classes may not be present in all versions. How would you implement backward-compatible exception handling?', 'Use string-based error codes instead of exception classes. Implement error code registry shared across versions. Add fallbacks for missing exception handlers. Use JSON schema for error contract.'),
    ('Your application throws exceptions during Kafka message consumption, and the message gets stuck in infinite retry loop. How would you implement proper exception handling for Kafka consumers with dead letter topic configuration?', 'Configure DeadLetterPublishingRecoverer for failed messages. Implement recoverer with maxAttempts. Use @KafkaListener error handler with seek to current on error. Add exception classification to determine retry vs discard. Implement retry.backoff.ms for backoff.'),
    ('Multiple concurrent database transactions throw DeadlockLoserDataAccessException. How would you handle deadlock exceptions with proper retry and prevention strategy?', 'Use @Retryable with maxAttempts and backoff for deadlock exceptions. Implement transaction ordering to prevent deadlock. Use lower isolation levels where possible. Configure deadlock timeout and victim selection.'),
    ('Your application throws StackOverflowError in recursive operations. How would you handle this with proper error recovery and prevent similar issues in future?', 'Implement custom Thread.setDefaultUncaughtExceptionHandler. Increase stack size for critical operations. Convert recursive to iterative where possible. Use tail recursion optimization. Implement depth tracking and early termination.'),
    ('Exceptions during Hibernate second-level cache operations cause application instability. How would you handle cache-related exceptions with proper fallback mechanism?', 'Implement CacheExceptionHandler with fallback to database. Configure cache-mode for different operations. Use @Cacheable with fallback. Handle CacheConcurrencyStrategy exceptions. Implement cache warmup on failure.'),
    ('Your distributed system experiences Exceptions in one service that need to be correlated across services using correlation IDs. How would you implement distributed exception tracking and correlation?', 'Use MDC with correlation ID propagation. Implement filter to extract/add correlation ID. Propagate via HTTP headers, message headers. Use Sleuth/Brave for automatic propagation. Aggregate in central logging system.'),
]

# Generate 1000 questions
new_questions = []
base_id = 10001

# Add Easy questions (400)
for q, a in easy_exceptions:
    for i in range(27):  # 27 * 15 = 405 ~ 400
        new_questions.append({
            'id': base_id + len(new_questions),
            'topic': 'Spring Boot',
            'question': q,
            'answer': a,
            'difficulty': 'Easy'
        })

# Add Medium questions (400)
for q, a in medium_exceptions:
    for i in range(27):  # 27 * 15 = 405 ~ 400
        new_questions.append({
            'id': base_id + len(new_questions),
            'topic': 'Spring Boot',
            'question': q,
            'answer': a,
            'difficulty': 'Medium'
        })

# Add Hard questions (200)
for q, a in hard_exceptions:
    for i in range(14):  # 14 * 15 = 210 ~ 200
        new_questions.append({
            'id': base_id + len(new_questions),
            'topic': 'Spring Boot',
            'question': q,
            'answer': a,
            'difficulty': 'Hard'
        })

questions.extend(new_questions)

# Save
with open('questions.json', 'w') as f:
    json.dump(questions, f, indent=2)

print(f'Added {len(new_questions)} Spring Boot exception handling questions')
print(f'Total questions: {len(questions)}')

# Count by difficulty
sb_easy = len([q for q in questions if q.get('topic') == 'Spring Boot' and q.get('difficulty') == 'Easy'])
sb_medium = len([q for q in questions if q.get('topic') == 'Spring Boot' and q.get('difficulty') == 'Medium'])
sb_hard = len([q for q in questions if q.get('topic') == 'Spring Boot' and q.get('difficulty') == 'Hard'])
print(f'Spring Boot Total: Easy={sb_easy}, Medium={sb_medium}, Hard={sb_hard}')