<h1>AWS S3 + Cloudfront Static Website hosting</h1>

<h2>Overview</h2>
This project demonstrates hosting a static website using **Amazon S3**, distributed securely via **Amazon CloudFront**, with optional **Route 53** DNS routing and **ACM** for SSL/TLS. This serverless architecture is designed for high availability and low latency.

<h2>Prerequisites</h2>
<bullet>AWS Free Tier Account</bullet>
<bullet>A simple static website for testing</bullet>
<bullet>(Optional) Route 53 + ACM for custom domain setup</bullet>

## Deployment Architecture - S3 → CloudFront → (Optional) Route 53 + ACM (Serverless) 
1.  **S3:** Origin bucket enabled for Static Website Hosting, containing the core HTML, CSS, JavaScript, and image assets.
2.  **CloudFront:** Content Delivery Network (CDN) that globally caches website content at Edge Locations for high-speed delivery and uses a secure SSL/TLS connection.
3.  **Route 53 + ACM:** Used to manage the **Custom Domain DNS** records and provision a **free SSL/TLS certificate** (via ACM) for HTTPS on CloudFront.
   
## Deletion Steps
1. Disable and Delete CloudFront distribution  
2. Empty and delete the S3 bucket 
3. Delete ACM certificate (if created)  
4. Delete the Route 53 hosted zone (if created)
