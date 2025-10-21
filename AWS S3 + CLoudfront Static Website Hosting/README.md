<h1>AWS S3 + Cloudfront Static Website hosting</h1>

<h2>Overview</h2>
This project demonstrates hosting a static website using **Amazon S3**, distributed securely via **Amazon CloudFront**, with optional **Route 53** DNS routing and **ACM** for SSL/TLS.

<h2>Prerequisites</h2>
<bullet>AWS Free Tier Account</bullet>
<bullet>A simple static website for testing</bullet>
<bullet>(Optional) Route 53 + ACM for custom domain setup</bullet>

## Architecture S3 → CloudFront → (Optional) Route 53 + ACM
1. S3 - Origin where static website files and other assets (like images) are present
2. Cloudfront - Caches website content over edge locations and delivers to users with low latency via a secure SSL/TLS connection
3. Route 53 + ACM - Used for DNS validation and custom domain setup
   
## Deletion Steps
1. Disable and Delete CloudFront distribution  
2. Empty and delete the S3 bucket 
3. Delete ACM certificate (if created)  
4. Delete the Route 53 hosted zone (if created)
