#!/usr/bin/env python3
"""Add Spring Boot Q&A from GeeksforGeeks article to questions.json with deduplication."""
import json, os, re

QUESTIONS_JSON = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'questions.json')

questions = [
    # === SPRING BOOT INTERVIEW QUESTIONS FOR FRESHERS ===
    {
        "topic": "Spring Boot",
        "difficulty": "Easy",
        "question": "What is Spring Boot?",
        "answer": "Spring Boot is built on top of the Spring framework to create stand-alone RESTful web applications with very minimal configuration. There is no need of external servers to run the application because it has embedded servers like Tomcat and Jetty. Spring Boot is independent and creates executable spring applications that are production-grade."
    },
    {
        "topic": "Spring Boot",
        "difficulty": "Medium",
        "question": "What are the features of Spring Boot?",
        "answer": "Key features: 1) Auto-configuration - automatically configures dependencies using @EnableAutoconfiguration annotation. 2) Spring Boot Starter POM - pre-configured dependencies for functions like database, security, maven configuration. 3) Spring Boot CLI (Command Line Interface) - manages dependencies, creates projects and runs applications. 4) Actuator - provides health check, metrics and monitors endpoints. 5) Embedded Servers - contains embedded Tomcat and Jetty servers, no need for external servers."
    },
    {
        "topic": "Spring Boot",
        "difficulty": "Easy",
        "question": "What are the advantages of using Spring Boot?",
        "answer": "Advantages: 1) Easy to use - most boilerplate code is reduced. 2) Rapid Development - opinionated approach and auto-configuration enable quick development. 3) Scalable - applications can be easily scaled up or down. 4) Production-ready - includes metrics, health checks, and externalized configuration designed for production environments."
    },
    {
        "topic": "Spring Boot",
        "difficulty": "Easy",
        "question": "Define the key components of Spring Boot.",
        "answer": "The key components are: Spring Boot Starters, Auto-configuration, Spring Boot Actuator, Spring Boot CLI, and Embedded Servers (Tomcat, Jetty)."
    },
    {
        "topic": "Spring Boot",
        "difficulty": "Easy",
        "question": "Why do we prefer Spring Boot over Spring?",
        "answer": "Spring Boot is preferred over Spring because: it's easier to use with less complexity, more production-ready with built-in metrics and health checks, more scalable, faster development with auto-configuration, and more customizable with opinionated defaults."
    },
    {
        "topic": "Spring Boot",
        "difficulty": "Medium",
        "question": "Explain the internal working of Spring Boot.",
        "answer": "Main steps: 1) Create a new Spring Boot project. 2) Add necessary dependencies. 3) Annotate the application with appropriate annotations (like @SpringBootApplication). 4) Run the application. Spring Boot automatically configures the application based on dependencies in the classpath and bootstraps the embedded server."
    },
    {
        "topic": "Spring Boot",
        "difficulty": "Easy",
        "question": "What are the Spring Boot Starter Dependencies?",
        "answer": "Commonly used starter dependencies: Data JPA starter, Web starter, Security starter, Test Starter, and Thymeleaf starter. These starters include pre-configured dependencies, version control, and configuration needed to make certain features work."
    },
    {
        "topic": "Spring Boot",
        "difficulty": "Medium",
        "question": "How does a Spring application get started?",
        "answer": "A Spring application starts by calling the main() method with @SpringBootApplication annotation in the SpringApplication class. This method takes a SpringApplicationBuilder object as a parameter to configure the application. Once the SpringApplication object is created, the run() method is called, which initializes the application context and starts the embedded web server."
    },
    {
        "topic": "Spring Boot",
        "difficulty": "Medium",
        "question": "What does the @SpringBootApplication annotation do internally?",
        "answer": "@SpringBootApplication combines three annotations: @Configuration (configures beans and packages), @EnableAutoConfiguration (automatically configures beans based on classpath dependencies), and @ComponentScan (scans components in the package and sub-packages). It automatically configures the application based on dependencies and bootstraps it using the run() method."
    },
    {
        "topic": "Spring Boot",
        "difficulty": "Easy",
        "question": "What is Spring Initializr?",
        "answer": "Spring Initializr is a tool that helps create the skeleton or project structure of a Spring Boot project by providing a Maven or Gradle file to build the application. It sets up the framework from scratch."
    },
    {
        "topic": "Spring Boot",
        "difficulty": "Easy",
        "question": "What are Spring Boot CLI and the most used CLI commands?",
        "answer": "Spring Boot CLI is a command-line tool used to create, run, and manage Spring Boot applications. It is built on top of the Groovy programming language. Most used CLI commands are: -run, -test, -jar, -war, --init, and -help."
    },

    # === SPRING BOOT INTERMEDIATE INTERVIEW QUESTIONS ===
    {
        "topic": "Spring Boot",
        "difficulty": "Medium",
        "question": "What are the basic Spring Boot Annotations?",
        "answer": "Basic annotations: @SpringBootApplication (main bootstrap annotation combining @Configuration, @EnableAutoConfiguration, @ComponentScan), @Configuration (indicates a class contains configuration methods), @Component (generic annotation for any Spring-managed component), @RestController (defines RESTful web service controller), @RequestMapping (maps HTTP requests to controller methods)."
    },
    {
        "topic": "Spring Boot",
        "difficulty": "Medium",
        "question": "What is Spring Boot dependency management?",
        "answer": "Spring Boot dependency management makes it easier to manage dependencies by ensuring all necessary dependencies are appropriate for the current Spring Boot version and compatible with it. For example, adding the Spring Boot starter web dependency automatically pulls in all web-related dependencies with compatible versions."
    },
    {
        "topic": "Spring Boot",
        "difficulty": "Easy",
        "question": "Is it possible to change the port of the embedded Tomcat server in Spring Boot?",
        "answer": "Yes, it is possible to change the port by setting the server.port property in the application.properties file. For example: server.port=8081 changes the port to 8081."
    },
    {
        "topic": "Spring Boot",
        "difficulty": "Easy",
        "question": "What is the starter dependency of the Spring Boot module?",
        "answer": "Spring Boot Starters are pre-configured Maven dependencies that make it easier to develop specific types of applications. They include dependencies, version control, and configuration. To use one, add it to pom.xml, e.g., spring-boot-starter-web for web applications."
    },
    {
        "topic": "Spring Boot",
        "difficulty": "Easy",
        "question": "What is the default port of Tomcat in Spring Boot?",
        "answer": "The default port of the embedded Tomcat server in Spring Boot is 8080. It can be changed by setting the server.port property in application.properties."
    },
    {
        "topic": "Spring Boot",
        "difficulty": "Medium",
        "question": "Can we disable the default web server in the Spring Boot application?",
        "answer": "Yes, we can disable the default web server in a Spring Boot application by setting the server.port property to -1 in the application.properties file."
    },
    {
        "topic": "Spring Boot",
        "difficulty": "Medium",
        "question": "How to disable a specific auto-configuration class?",
        "answer": "To disable a specific auto-configuration class, use the @EnableAutoConfiguration annotation with the exclude attribute: @EnableAutoConfiguration(exclude = {ClassName.class})"
    },
    {
        "topic": "Spring Boot",
        "difficulty": "Easy",
        "question": "Can we create a non-web application in Spring Boot?",
        "answer": "Yes, Spring Boot can create non-web applications such as Microservices, Console applications, and batch applications. Spring Boot is not limited to web applications only."
    },
    {
        "topic": "Spring Boot",
        "difficulty": "Medium",
        "question": "Describe the flow of HTTP requests through the Spring Boot application.",
        "answer": "1) Client makes an HTTP request (GET, POST, PUT, DELETE) to the browser. 2) The request goes to the controller where requests are mapped and handled. 3) In the Service layer, business logic is performed on data mapped to JPA using model classes. 4) In the repository layer, CRUD operations are performed for REST APIs. 5) A JSP page is returned to the end user if there are no errors."
    },
    {
        "topic": "Spring Boot",
        "difficulty": "Medium",
        "question": "Explain @RestController annotation in Spring Boot.",
        "answer": "@RestController is a shortcut for building RESTful services. It combines @Controller (marks the class as a request handler in Spring MVC) and @ResponseBody (tells Spring to convert method return values directly into HTTP responses instead of rendering views). It enables defining endpoints for HTTP methods (GET, POST, PUT, DELETE) and returning data in formats like JSON or XML."
    },
    {
        "topic": "Spring Boot",
        "difficulty": "Medium",
        "question": "Difference between @Controller and @RestController.",
        "answer": "@Controller is used for web applications to mark a class as a controller, used with @RequestMapping to map HTTP requests to methods. @RestController combines @Controller and @ResponseBody, used for RESTful APIs to handle GET, PUT, POST, DELETE requests. @RestController prioritizes data responses for building APIs, while @Controller returns views for web applications."
    },
    {
        "topic": "Spring Boot",
        "difficulty": "Easy",
        "question": "What is the difference between @RequestMapping and @GetMapping?",
        "answer": "@RequestMapping handles various HTTP request methods (GET, POST, etc.) with method attribute specifying the type, e.g., @RequestMapping(value='/example', method=RequestMethod.GET). @GetMapping is a specialized shortcut that handles only HTTP GET requests, e.g., @GetMapping('/example')."
    },
    {
        "topic": "Spring Boot",
        "difficulty": "Medium",
        "question": "What are the differences between @SpringBootApplication and @EnableAutoConfiguration annotation?",
        "answer": "@SpringBootApplication is typically used on the main class as the entry point. It includes @ComponentScan to enable component scanning. @EnableAutoConfiguration can be used on any configuration class, does not perform component scanning by itself. @SpringBootApplication is used when you want auto-configuration with component scanning; @EnableAutoConfiguration is used when you want to customize auto-configuration without component scanning."
    },
    {
        "topic": "Spring Boot",
        "difficulty": "Medium",
        "question": "What are Profiles in Spring?",
        "answer": "Spring Profiles are different configurations for different environments (development, testing, production). You define sets of configurations (like database URLs) for different situations using the @Profile annotation. Profiles are activated by setting the spring.profiles.active property via environment variables or command-line options."
    },
    {
        "topic": "Spring Boot",
        "difficulty": "Medium",
        "question": "Mention the differences between WAR and embedded containers.",
        "answer": "WAR: Contains all files needed to deploy a web application to a web server. Requires external configuration files (web.xml, context.xml). Deployed to a web server with security features. Embedded containers: The web application server is included in the same JAR file as the application code. Uses configuration properties or annotations within the code. Can be made more secure using JRE security features."
    },

    # === SPRING BOOT INTERVIEW QUESTIONS FOR EXPERIENCED ===
    {
        "topic": "Spring Boot",
        "difficulty": "Hard",
        "question": "What is Spring Boot Actuator?",
        "answer": "Spring Boot Actuator is a component that provides production-ready operational monitoring and management capabilities. It enables managing and monitoring a Spring Boot application while it is running. To use it, add the spring-boot-starter-actuator dependency to the project."
    },
    {
        "topic": "Spring Boot",
        "difficulty": "Hard",
        "question": "How to enable Actuator in the Spring Boot application?",
        "answer": "Steps: 1) Add the Actuator dependency (spring-boot-starter-actuator) to pom.xml. 2) Enable endpoints in application.properties. 3) Run the Spring Boot app. Actuator endpoints can then be accessed at URLs on the management port."
    },
    {
        "topic": "Spring Boot",
        "difficulty": "Medium",
        "question": "What is the purpose of using @ComponentScan in the class files?",
        "answer": "@ComponentScan tells Spring to scan a package and automatically detect Spring components, configurations, and services. It can be used in three ways: 1) Without arguments - scans the current package. 2) With basePackageClasses - specifies classes whose packages should be scanned. 3) With basePackages - specifies package names to scan."
    },
    {
        "topic": "Spring Boot",
        "difficulty": "Medium",
        "question": "What are the @RequestMapping and @RestController annotations in Spring Boot used for?",
        "answer": "@RequestMapping maps HTTP requests to handler methods in controller classes. It can be used at class and method level, supporting mapping by HTTP method (GET, POST, PUT, DELETE), URL path, URL parameters, and request headers. @RestController is a convenience annotation combining @Controller and @ResponseBody, indicating a controller where every method returns a domain object instead of a view."
    },
    {
        "topic": "Spring Boot",
        "difficulty": "Medium",
        "question": "How to get the list of all the beans in your Spring Boot application?",
        "answer": "Using the ApplicationContext object in Spring Boot, you can retrieve a list of all the beans in the application. The ApplicationContext is responsible for managing beans and their dependencies. You can autowire ApplicationContext and call getBeanDefinitionNames() to get all bean names."
    },
    {
        "topic": "Spring Boot",
        "difficulty": "Medium",
        "question": "Can we check the environment properties in your Spring Boot application? Explain how.",
        "answer": "Yes, the Environment object in a Spring Boot application can be used to check environment properties. The Environment object contains configuration settings from property files, command-line arguments, and environment variables. You can get the Environment instance by calling the getEnvironment() method on the ApplicationContext."
    },
    {
        "topic": "Spring Boot",
        "difficulty": "Medium",
        "question": "How to enable debugging log in the Spring Boot application?",
        "answer": "Steps: 1) Add the logging level property to application.properties (logging.level.root=DEBUG). 2) Configure the log pattern. 3) Run the application. The log level can also be changed at runtime using the Actuator endpoint: curl -X POST http://localhost:8080/actuator/loggers/<logger-name> -H 'content-type: application/json' -d '{\"configuredLevel\": \"DEBUG\"}'."
    },
    {
        "topic": "Spring Boot",
        "difficulty": "Medium",
        "question": "What is dependency injection and its types?",
        "answer": "Dependency Injection (DI) is a design pattern that enables loosely coupled components. An object's ability to complete a task depends on another object. Three types: 1) Constructor injection - dependency is injected through the constructor (most common in Spring Boot). 2) Setter injection - dependency is injected through setter methods. 3) Field injection - dependency is injected directly into the field."
    },
    {
        "topic": "Spring Boot",
        "difficulty": "Medium",
        "question": "What is an IoC container?",
        "answer": "An IoC (Inversion of Control) Container in Spring Boot is a central manager for application objects. It controls the creation, configuration, and management of dependency injection of objects (beans). It is also referred to as a DI (Dependency Injection) container."
    },
    {
        "topic": "Spring Boot",
        "difficulty": "Hard",
        "question": "What is the difference between Constructor and Setter Injection?",
        "answer": "Constructor Injection: Dependencies are provided through constructor parameters. Promotes immutability as dependencies are set at creation. Harder to override dependencies. Setter Injection: Dependencies are set through setter methods after object creation. Dependencies can be changed dynamically after object creation. Allows easier overriding of dependencies using different setter values."
    },

    # === BONUS SPRING BOOT INTERVIEW QUESTIONS ===
    {
        "topic": "Spring Boot",
        "difficulty": "Medium",
        "question": "What is Thymeleaf?",
        "answer": "Thymeleaf is a Java-based server-side template engine used in Java web applications to render dynamic web pages. It is a popular choice for server-side templating in the Spring ecosystem, including Spring Boot."
    },
    {
        "topic": "Spring Boot",
        "difficulty": "Medium",
        "question": "Explain Spring Data and what is Spring Data JPA?",
        "answer": "Spring Data is a powerful framework for developing data-oriented applications. It simplifies data-centric application development by offering abstractions, utilities, and integration with various data sources. Spring Data JPA is a subproject that provides support for accessing data from relational databases using JPA (Java Persistence API)."
    },
    {
        "topic": "Spring Boot",
        "difficulty": "Medium",
        "question": "Explain Spring MVC.",
        "answer": "Spring MVC (Model-View-Controller) is a web MVC framework built on top of the Spring Framework. Model represents the data, View renders the user interface, and Controller handles the request/response flow. It provides a comprehensive programming model for building web applications."
    },
    {
        "topic": "Spring Boot",
        "difficulty": "Easy",
        "question": "What is a Spring Bean?",
        "answer": "A Spring Bean is any Java object that is managed by the Spring IoC container. The IoC container creates, configures, and manages the lifecycle of beans."
    },
    {
        "topic": "Spring Boot",
        "difficulty": "Hard",
        "question": "What are Inner Beans in Spring?",
        "answer": "An Inner Bean refers to a bean defined within the scope of another bean's definition. It is declared inside the configuration of another bean without explicitly giving it a unique identifier. Inner Beans are defined as nested <bean> elements within the enclosing bean's configuration."
    },
    {
        "topic": "Spring Boot",
        "difficulty": "Hard",
        "question": "What is Bean Wiring?",
        "answer": "Bean wiring is a mechanism in Spring for managing dependencies between beans. It allows Spring to inject collaborating beans into each other. There are two types: Autowiring (Spring automatically resolves dependencies) and Manual wiring (dependencies are explicitly configured)."
    },
    {
        "topic": "Spring Boot",
        "difficulty": "Medium",
        "question": "What are Spring Boot DevTools used for?",
        "answer": "Spring Boot DevTools provides development-time features: 1) Automatic application restart when code changes. 2) Fast application startup. 3) Actuator endpoints for monitoring. 4) Additional development utilities to increase developer productivity."
    },
    {
        "topic": "Spring Boot",
        "difficulty": "Easy",
        "question": "What error do you see if H2 is not present in the classpath?",
        "answer": "If H2 is not present in the classpath, you will see: java.lang.ClassNotFoundException: org.h2.Driver."
    },
    {
        "topic": "Spring Boot",
        "difficulty": "Medium",
        "question": "Mention the steps to connect the Spring Boot application to a database using JDBC.",
        "answer": "Steps: 1) Add the JDBC driver dependency for the database (e.g., MySQL Connector). 2) Create an application.properties file. 3) Configure database connection properties (URL, username, password). 4) Create a JdbcTemplate bean. 5) Use the JdbcTemplate bean to execute SQL queries and statements."
    },
    {
        "topic": "Spring Boot",
        "difficulty": "Medium",
        "question": "Mention the advantages of YAML file over Properties file and the different ways to load YAML in Spring Boot.",
        "answer": "Advantages of YAML: Easy to edit and modify, concise syntax, supports complex data types (lists, maps). Ways to load YAML in Spring Boot: 1) Using @ConfigurationProperties annotation. 2) Using YamlPropertiesFactoryBean class."
    },
    {
        "topic": "Spring Boot",
        "difficulty": "Hard",
        "question": "What do you understand about Spring Data REST?",
        "answer": "Spring Data REST is a framework that exposes Spring Data repositories as RESTful web services. It allows exposing repositories as REST endpoints with minimal configuration by following Spring Data REST technologies like Spring Data and Spring MVC."
    },
    {
        "topic": "Spring Boot",
        "difficulty": "Hard",
        "question": "Why is Spring Data REST not recommended in real-world applications?",
        "answer": "Reasons: 1) Performance may not be optimal for very large-scale applications. 2) Versioning REST APIs exposed by Spring Data REST can be difficult. 3) Handling relationships between entities can be tricky. 4) Limited options for filtering results returned by endpoints."
    },
    {
        "topic": "Spring Boot",
        "difficulty": "Hard",
        "question": "How is Hibernate chosen as the default implementation for JPA without any configuration?",
        "answer": "Spring Boot automatically configures Hibernate as the default JPA implementation when the spring-boot-starter-data-jpa dependency is added. This dependency includes the Hibernate JAR file and Spring Boot auto-configuration for JPA, which detects Hibernate in the classpath and configures it as the JPA provider."
    },
    {
        "topic": "Spring Boot",
        "difficulty": "Hard",
        "question": "Explain how to deploy to a different server with Spring Boot.",
        "answer": "Steps: 1) Build the Spring Boot application (e.g., mvn clean package to create a JAR/WAR). 2) Create a deployment package. 3) Deploy the deployment package to the target server (copy the JAR/WAR). 4) Start the server (run java -jar app.jar or deploy WAR to a servlet container like Tomcat)."
    }
]

def main():
    # Load existing questions
    with open(QUESTIONS_JSON, 'r', encoding='utf-8') as f:
        existing = json.load(f)

    print(f"Existing questions: {len(existing)}")

    # Build dedup set
    existing_texts = set()
    for q in existing:
        key = q['question'].lower().strip()
        existing_texts.add(key)

    # Filter new questions
    next_id = max(q['id'] for q in existing) + 1 if existing else 1
    added = 0
    skipped = 0

    for q in questions:
        key = q['question'].lower().strip()
        if key not in existing_texts:
            existing_texts.add(key)
            q['id'] = next_id
            next_id += 1
            existing.append(q)
            added += 1
        else:
            skipped += 1

    # Write back
    with open(QUESTIONS_JSON, 'w', encoding='utf-8') as f:
        json.dump(existing, f, indent=2, ensure_ascii=False)

    print(f"Added: {added}, Skipped (duplicates): {skipped}")
    print(f"Total: {len(existing)}")

    # Topic counts
    topics = {}
    for q in existing:
        topics[q['topic']] = topics.get(q['topic'], 0) + 1
    print("\n=== TOPIC COUNTS ===")
    for t, c in sorted(topics.items()):
        print(f"  {t}: {c}")

if __name__ == '__main__':
    main()
