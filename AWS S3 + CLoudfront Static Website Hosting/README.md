<h1>AWS S3 + Cloudfront Static Website hosting</h1>

<h2>Overview</h2>
This project demonstrates hosting a static website using **Amazon S3**, distributed securely via **Amazon CloudFront**, with optional **Route 53** DNS routing and **ACM** for SSL/TLS. This serverless architecture is designed for high availability and low latency.

<h2>Prerequisites</h2>
1. AWS Free Tier Account
2. A simple static website for testing 
- (I used a website I developed for my MSCS project: https://pavanijl.github.io)
3. (Optional) Route 53 + ACM for custom domain setup

## Architecture Cloudfront → S3 → (Optional) Route 53 + ACM (Serverless) 

1.  **S3:** Origin bucket enabled for Static Website Hosting, containing the core HTML, CSS, JavaScript, and image assets.
2.  **CloudFront:** Content Delivery Network (CDN) that globally caches website content at Edge Locations for high-speed delivery and uses a secure SSL/TLS connection.
3.  **Route 53 + ACM:** Used to manage the **Custom Domain DNS** records and provision a **free SSL/TLS certificate** (via ACM) for HTTPS on CloudFront.

## 🪣 Step 1: Create and Configure an S3 Bucket

1. Go to **S3 → Create bucket**
   - Bucket name must be **unique globally** (e.g., `my-demo-site`).
   - **Region:** Choose one close to you.
2. **Uncheck** “Block all public access.”
3. Upload your website files (`index.html`, `styles.css`, `content.js`, images, etc.).
4. Under **Properties → Static website hosting**:
   - Enable *Static website hosting*.
   - Choose **Host a static website**.
   - Enter:
     - Index document: `index.html`
     - Error document: `error.html` (leave blank if none)
5. Copy the **Bucket website endpoint** — this is the direct public website URL.

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
   - Origin domain: Select your S3 bucket’s static website endpoint (not the default S3 bucket URL).
   - Viewer protocol policy: Redirect HTTP to HTTPS
3. Under Default cache behavior:
   - Allowed HTTP methods: GET, HEAD
4. Under Settings:
   - Alternate domain name (CNAME): (optional) Add your custom domain (e.g., example.tk)
   - SSL Certificate:
      a) Select “Default CloudFront certificate (*.cloudfront.net)”
         OR
      b) Choose your issued ACM certificate (if using custom domain).
5. Click Create distribution.
6. Wait until the status becomes Deployed.
7. Test your site using the CloudFront domain URL (e.g., d123abc.cloudfront.net).

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

## Demo Preview
## 💡 Example URLs
 
| Stage                          | URL Example                                                                                                |
| ------------------------------ | ---------------------------------------------------------------------------------------------------------- |
| S3 Static Site                 | [http://my-bucket.s3-website-us-east-1.amazonaws.com](http://my-bucket.s3-website-us-east-1.amazonaws.com) |
| CloudFront                     | [https://d1234abcd.cloudfront.net](https://d1234abcd.cloudfront.net)                                       |
| Custom Domain (Route 53 + ACM) | [https://customsite.com](https://customsite.com)                                                                   |


