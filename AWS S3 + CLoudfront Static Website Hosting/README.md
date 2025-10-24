# Static website hosting using S3 + CloudFront + (Optional for custom domain) Route 53 + ACM 

Static website hosting using:
1) Only AWS S3 (Why not the recommended approach) 
2) S3 + Cloudfront (recommended approach) + (Optional setup if using custom domain) Route 53 + ACM

<h2>Prerequisites</h2>
1. AWS Free Tier Account

2. A simple static website for testing 
- (I used a website I developed for my MSCS project: https://pavanijl.github.io)

3. (Optional) Route 53 + ACM for custom domain setup

<h1>Part1: Static website hosting using only AWS S3</h1>

<h2>Overview</h3>
Setting up a static website using just AWS S3 bucket and no other services

## 🪣 Step 1: Create and Configure an S3 Bucket

1. Go to **S3 → Create bucket**
   - Bucket name: `my-static-site`.
2. **Uncheck** “Block all public access.”
3. Upload your website files (`index.html`, `styles.css`, `content.js`, images, etc.).
4. Under **Properties → Static website hosting**:
   - Enable *Static website hosting*.
   - Choose **Host a static website**.
   - Enter:
     - Index document: `index.html`
     - Error document: `error.html` or leave blank if none
5. Copy the **Bucket website endpoint** — this is the direct public website URL.

---

## 🔐 Step 2: Set Bucket Policy (Make Files Public)

Go to **Permissions → Bucket Policy**, and paste below json:

```
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "PublicReadGetObject",
      "Effect": "Allow",
      "Principal": "*",
      "Action": "s3:GetObject",
      "Resource": "arn:aws:s3:::your-bucket-name/*"
    }
  ]
}
```

Disadvantages of using only S3 for static website hosting in comparision with using Cloudfront + S3

| Step                       | S3 Static Website (Direct)                                        | S3 + CloudFront (Recommended)                                                                                                                                                  |
| -------------------------- | ----------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Static website hosting** | ✅ Must be **enabled** (S3 serves files directly to the internet). | ❌ **Keep disabled** — CloudFront fetches content using the bucket origin endpoint, not the website endpoint.                                                                   |
| **Public access settings** | ❌ Must allow public access (so users can reach files directly).   | ✅ **Keep “Block all public access” enabled.** CloudFront accesses S3 using an **Origin Access Control (OAC)** or **Origin Access Identity (OAI)** — no need for public access. |
| **Bucket Policy**          | Required to allow `s3:GetObject` for everyone.                    | Not required (CloudFront authenticates internally to fetch files securely).                                                                                                    |
| **Security**               | No HTTPS by default — only HTTP.                                  | HTTPS via CloudFront + ACM — secure by default.                                                                                                                                |
| **Performance**            | Region-bound, slower globally.          


<h1>Part2: AWS S3 + Cloudfront Static Website hosting</h1>

<h2>Overview</h2>
This project demonstrates hosting a static website using **Amazon S3**, distributed securely via **Amazon CloudFront**, with optional **Route 53** DNS routing and **ACM** for SSL/TLS. This serverless architecture is designed for high availability and low latency.

## Architecture Cloudfront → S3 → (Optional) Route 53 + ACM (Serverless) 

1.  **S3:** Origin bucket enabled for Static Website Hosting, containing the core HTML, CSS, JavaScript, and image assets.
2.  **CloudFront:** Content Delivery Network (CDN) that globally caches website content at Edge Locations for high-speed delivery and uses a secure SSL/TLS connection.
3.  **Route 53 + ACM:** Used to manage the **Custom Domain DNS** records and provision a **free SSL/TLS certificate** (via ACM) for HTTPS on CloudFront.

## Architecture Diagram
Note: Diagram created using draw.io ([diagrams.net](https://app.diagrams.net/)) with AWS icon library enabled.

[Architecture Diagram](./s3-cloudfront-static-website.png)  
Editable file: [`architecture-diagram.drawio`](./s3-cloudfront-static-website.drawio)

## 🪣 Step 1: Create and Configure an S3 Bucket

1. Go to **S3 → Create bucket**
   - Bucket name: `my-static-site`.
   - Keep Block all public access ✅ (don’t uncheck it).
2. Upload your static files (`index.html`, `styles.css`, `content.js`, images, etc.).
3. Do NOT enable Static website hosting
4. No need to add a bucket policy manually — CloudFront will use a secure identity to access the bucket..

## 🔐 Step 2: Set Bucket Policy (Make Files Public)

Go to **Permissions → Bucket Policy**, and paste below json:
```
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "PublicReadGetObject",
      "Effect": "Allow",
      "Principal": "*",
      "Action": "s3:GetObject",
      "Resource": "arn:aws:s3:::your-bucket-name/*"
    }
  ]
}
```
## 🌍 Step 3: Create Cloudfront Distribution

1. Go to CloudFront → Create Distribution
2. Under Origin settings:
   - Origin domain: select your S3 bucket (the plain name, not the “website endpoint”).
Example: my-static-site.s3.us-east-1.amazonaws.com
3. Origin Access: choose Origin Access Control (OAC).
CloudFront will create and attach a secure OAC to access the S3 bucket
4.Viewer Protocol Policy: Redirect HTTP to HTTPS.
5. Cache Policy: use the CachingOptimized default.
6. Under Settings:
   - Alternate domain name (CNAME): (optional) Add your custom domain (e.g., example.tk)
   - SSL Certificate:
      a) Select “Default CloudFront certificate (*.cloudfront.net)”
         OR
      b) Choose your issued ACM certificate (if using custom domain).
7. Click Create distribution.
8. Wait until the status becomes Deployed.
9. Test your site using the CloudFront domain URL (e.g., d123abc.cloudfront.net).

## 🔒 Step 4: (Optional if using custom domain) Request ACM Certificate for HTTPS

1. Go to AWS Certificate Manager (ACM) → Request a public certificate.
2. Add domain names:
   - mycustomsite.com
   - *.mycustomsite.com
3. Choose DNS validation.
4. Copy the generated CNAME record (Name + Value).
5. Go to Route 53 → Hosted zones → YourDomain → Create record:
   - Type: CNAME
   - Paste the Name and Value from ACM.
6. Once validated, ACM status changes from Pending Validation → Issued.

## 🌐 Step 5: (Optional if using custom domain) Configure Route 53 for custom domain

If you already have a domain (via free domain provider or Route 53):
1. In Route 53 → Hosted zones → Create hosted zone
   - Domain name: mycustomsite.com
   - Type: Public hosted zone
2. Create A record (Alias):
   - Record name: leave blank or type www
   - Record type: A – IPv4 address
   - Alias: Yes
   - Alias target: select your CloudFront distribution
3. (If free domain domain):
   - Go to Freenom → Manage Domain → Manage DNS
   - Add Name Servers (NS) from Route 53 Hosted Zone.
4. Wait for DNS propagation (can take 15–30 minutes).   
5.Access your website via your custom domain (e.g., https://mycustomsite.com).

## Deletion Steps

1. Disable and Delete CloudFront distribution  
2. Empty and delete the S3 bucket 
3. Delete ACM certificate (if created)  
4. Delete the Route 53 hosted zone (if created)

## 💡 Example URLs
 
| Stage                          | URL Example                                                                                                |
| ------------------------------ | ---------------------------------------------------------------------------------------------------------- |
| S3 Static Site                 | [http://my-bucket.s3-website-us-east-1.amazonaws.com](http://my-bucket.s3-website-us-east-1.amazonaws.com) |
| CloudFront                     | [https://d1234abcd.cloudfront.net](https://d1234abcd.cloudfront.net)                                       |
| Custom Domain (Route 53 + ACM) | [https://customsite.com](https://customsite.com)                                                                   |
## References
Amazon S3 (Static Website Hosting)

[Host a static website using Amazon S3](https://docs.aws.amazon.com/AmazonS3/latest/userguide/WebsiteHosting.html)

[Granting read-only permission to an anonymous user](https://docs.aws.amazon.com/AmazonS3/latest/userguide/WebsiteAccessPermissionsReqd.html)

Amazon CloudFront

[Getting started with a CloudFront web distribution](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/GettingStarted.html)

[Using CloudFront with Amazon S3](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/DownloadDistS3AndCustomOrigins.html)

[Using alternate domain names (CNAMEs)](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/CNAMEs.html)

AWS Certificate Manager (ACM)

[Requesting a public certificate](https://docs.aws.amazon.com/acm/latest/userguide/gs-acm-request-public.html)

[Validating domain ownership with DNS](https://docs.aws.amazon.com/acm/latest/userguide/dns-validation.html)

Amazon Route 53

[Registering domain names using Route 53](https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/domain-register.html)

[Routing traffic to an Amazon CloudFront distribution](https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/routing-to-cloudfront-distribution.html)

[Creating records by using the Route 53 console](https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/resource-record-sets-creating.html)

AWS Official Tutorials

[Tutorial: Configuring a static website using a custom domain registered with Route 53](https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/getting-started-cloudfront-overview.html)

