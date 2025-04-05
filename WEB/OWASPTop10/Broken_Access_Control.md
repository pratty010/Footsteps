# Access Control Control (OWASP TOP 10 #1)

## ACCESS CONTROL

_Access control_ is a _security mechanism_ used to control which users or systems are allowed to access a particular resource or system. Access control is implemented in computer systems to ensure that only authorized users have access to resources, such as files, directories, databases, and web pages. The primary goal of access control is to protect sensitive data and ensure that it is only accessible to those who are authorized to access it.

## COMMON MECHANISMS

1. **Discretionary Access Control (DAC):** In this type of access control, the resource owner or administrator determines who is allowed to access a resource and what actions they are allowed to perform. DAC is commonly used in operating systems and file systems. _It’s the liberty to control access to your own resources._
2. **Mandatory Access Control (MAC):** In this type of access control, access to resources is determined by a set of predefined rules or policies that are enforced by the system. MAC is commonly used in highly secure environments, such as government and military systems.
3. **Role-Based Access Control (RBAC):** In this type of access control, users are assigned roles that define their level of access to resources. RBAC is commonly used in enterprise systems, where users have different levels of authority based on their job responsibilities. That’s the essence of RBAC - assigning access based on a person’s role within an organization.
4. **Attribute-Based Access Control (ABAC):** In this type of access control, access to resources is determined by a set of attributes, such as user role, time of day, location, and device. ABAC is commonly used in cloud environments and web applications.


## BROKEN ACCESS CONTROL

Broken access control vulnerabilities refer to situations where access control mechanisms fail to enforce proper restrictions on user access to resources or data. Here are some common exploits for broken access control and examples:

1. **Horizontal privilege escalation** occurs when an attacker can access resources or data belonging to other users with the same level of access. For example, a user might be able to access another user’s account by changing the user ID in the URL.
2. **Vertical privilege escalation** occurs when an attacker can access resources or data belonging to users with higher access levels. For example, a regular user can access administrative functions by manipulating a hidden form field or URL parameter.
3. **Insufficient access control** checks occur when access control checks are not performed correctly or consistently, allowing an attacker to bypass them. For example, an application might allow users to view sensitive data without verifying their proper permissions.
4. **Insecure direct object references** occur when an attacker can access a resource or data by exploiting a weakness in the application’s access control mechanisms. For example, an application might use predictable or easily guessable identifiers for sensitive data, making it easier for an attacker to access.


## MITIGATIONS

1. **RBAC**
2. **Use Parameterized Queries:** Parameterized queries are a way to protect PHP applications from SQL Injection attacks, where malicious users could potentially gain unauthorized access to your database. By using placeholders instead of directly including user input into the SQL query, you can significantly reduce the risk of SQL Injection attacks.
3. **Proper Session Management:** Proper session management ensures that authenticated users have timely and appropriate access to resources, thereby reducing the risk of unauthorized access to sensitive information. Session management includes using secure cookies, setting session timeouts, and limiting the number of active sessions a user can have.
4. **Use Secure Coding Practices:** Secure coding practices involve methods to prevent the introduction of security vulnerabilities. Developers should sanitize and validate user input to prevent malicious data from causing harm and avoid using insecure functions or libraries.