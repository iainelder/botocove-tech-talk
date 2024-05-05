# fwd:cloudsec Europe 2024 Submission

Speaker name: Iain Elder

Presentation title: Botocove, or how I stopped my own denial-of-wallet attack via CloudTrail

Talk length: 20 minutes

Abstract:

AWS Organizations is the fundamental service for managing a large AWS estate, and integrates with many other management and governance services, such as Config, StackSets and CloudTrail. A mature operation takes advantage of these integrations to maintain a consistent baseline across even 1000s of accounts.

What if you are dropped into a growing or anarchic project where none of those integrations are active yet? Even if you have the power to enable them, fighting fires may leave you without time. You still need to report on resources and remediate bad ones. How do you do that?

In this talk I'll show you Botocove, my tactical solution to report and remediate even with minimal governance infrastructure.

Botocove is a tool for AWS organization administrators and security auditors who are also Python programmers. It runs a Boto3 function in parallel across selected accounts and regions and collects the results.

The first problem it solved for me was stopping my own accidental denial-of-wallet attack caused by an oversight while migrating from account-based trails to an organization trail. I'll give you a taste of Botocove's power revisting the steps I took to analyze and solve the org-wide problem.

Session details:

I expect the audience to be familiar with the AWS services I mention in the abstract and to be familiar with the boto3 SDK.

I'll introduce myself and describe botocove in a few words. I'll give a shout-out to Dave Connell, the original developer of Botocove, who is now an employee of AWS.

I'll start by reminding of the need for org-wide governance services. Then I'll describe situations in which they may not be available or where they may not meet our needs.

From there I'll discuss an expensive mistake I made on one project when migrating from account trails to an organization trail. I didn't turn off all the account trails until we noticed the big bill! It's a great example of a problem that AWS doesn't solve for you, that is easy enough to fix in a single account but hard to solve without automation across 1000 accounts.

Botocove is simple enough to use an interactive Python console, and that is how I will introduce the tool. I will show how to stop all the trails using Botocove in the Python console. To avoid external issues, I won't use a live Python console, but I'll show a series of code samples, each with a result that I prepared earlier in a test environment. Each result would have run in a Python terminal connected to my sandbox organization. Each result is simply the output of the main cove function, simplified so that the result remains readable for the whole audience.

I will refer to other solutions such as AWS Config and Steampipe to show where they are equivalent and where Botocove goes further. AWS Config doesn't record the IsLogging property. Steampipe does record IsLogging but doesn't allow you to change it, just read it. AWS Config does allow you to remediate through rules and Lambda functions but it requires a lot of setup. Botocove is the simplest solution I know for otherwise unmanaged trail resources.

I'll finish by playing devil's advocate, suggesting that Botocove is unnecessary because anyone can loop over AWS accounts - can't they? There are lots of ways to do it, and lots of traps to fall into, especially when using Boto3 in parallel. I'll point to some of the sharp edges in Boto3 that until recently were poorly undocumented, that caused memory leaks in Botocove severe enough to crash the tool in large environments. Solving that memory leak was coincidentally my first big contribution to the project.

Finally I'll give the audience a call to action: visit the GitHub repo and give us a star!

In February AWS enrolled me in its AWS New Voices program for public speakers. The mentors and fellow trainees have helped me to develop structures and techniques to engage audiences.

I first presented this session at the open-source booth at AWS Summit in London on 2024-04-24. It was the world's smallest stage, and not well promoted by AWS, but it was well received by the few who knew about it. I would love the opportunity to share my talk with a bigger audience who may relate to situations like mine.

In 20 minutes I have time to show just a single use and just the basic features of Botocove, so I welcome Q&A from the audience at the end if they want to know more about how it might solve a problem they have or other situations in which I have found it useful or if they want to suggest features to make it better.

Botocove project GitHub repo:

https://github.com/connelldave/botocove

You can preview the slides I used for the first version of this talk in another GitHub repo:

https://github.com/iainelder/botocove-tech-talk

Speaker bio:

Iain is an independent AWS consultant. He helps his clients to build landing zones, manage security posture, control costs, and develop custom automation solutions. In 2023 AWS named him a Community Builder, probably because he spends too much time on GitHub. There he contributes to Botocove and other open-source AWS tooling. You can follow him at https://github.com/iainelder/.

Detailed description:

How can the audience benefit from watching your talk live? Q&A.

This talk was first presented at the open source booth of the AWS Summit in London on 2024-04-24.

No special presentation facilities are required.

I accept to have my talk recorded.

Botocove is published under the LGPL-3.0 license.

I will publish the support material for the talk to a GitHub repo.
