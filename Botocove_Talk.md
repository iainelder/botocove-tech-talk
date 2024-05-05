# Botocove

1. Hook
2. Who are you
3. What will the audience get?
4. Why is it important?
5. Give one call to action

Three main takaways:

* An AWS organization's management complexity grows with the number of member accounts
* Don't write automation from scratch. It'll be slow or buggy or both.
* Use botocove to handle the complexity and let you focus on the use case

TODO:

* Where do I mention I'm a botocove maintainer? Maybe I set too much scene.
* Talk about dolphins. Can I adapt an Ecco the Dolphin grahic?

Imagine you're the new administrator of an AWS estate. The company's growth attracted you.A startup became a market leader. But attention is spread thin, and success has made the company a target. Management worries about security and compliance issues.

The IT environment has become complex and chaotic. The admins before you established minimal governance of billing and permissions using AWS Organizations. Beyond this nothing is formal. You need to establish a security baseline with governance services such as CloudTrail, AWS Config, and Security Hub. To do things right you needclean up the relics of a clickops culture while setting up new infrastructure with code and deployment pipelines. New accounts, teams, and services come online every month, and each one seems to make progress slower.

I put you in this scenario because I face it with every new customer. My name is Iain and I'm an independent AWS consultant. I see AWS customers big and small struggle with these awkward steps towards a mature security posture. My job is to guide customers on this journey to maximize their returns and protect their investment in AWS.

I'm also a contributer to the botocove project.

To win you need to build robust solutions that scale as the organization grows. To start you need a tool that in your minimal setup gets fast results to buy time to negotiate the long-term solutions.

In this session I'll share with you my secret tactical weapon: botocove.

Botocove is a power tool for AWS administrators who are also Python programmers. It takes any function you can write, runs it across all the AWS accounts in your organization, groups all the results together, and returns it in one big object.

Managing an an AWS organization is complex because to you need to perform every action in all organization member accounts to be sure you have full coverage.

Botocove is a way to solve that problem. All you need is AdministratorAccess in the organization management account and a role to assume in each of the member accounts.

You can set up governance services such as AWS Config and Security Hub to centralize the management of some use cases in a delegated admin account. But you may need something before you have these services set up. And you may need to solve use cases that these services don't support yet or were never designed for.

I will take you through two related case studies from my field work to show how botocove can help you work fast and thorough even in the largest environment. The first case I'll show you is my naive state, before I discovered botocove. This serves to show you how to solve the problem from first principles as a Python programmer and why you shouldn't do it yourself because of all the problems that you may run into, solutions to which botocove has codified from its users' experience and feedback.

The second is a similar use case after I discovered botocove, and how it helped me to achieve a result that would have been impossible without some form of automation and was quicker and more reliable than all the other solutions available to me.

---

Use cases:

* Dentsu: taking inventory of per-account trails to make the case for deploying an organization trail
* Volkswagen: decommissioning the VWAG trail

---

In 2021 I won my first big customer, Dentsu Tracking. They tasked me with taking control of the infrastructure, the costs, and the security.

At the time Dentsu had an estate of about 50 AWS accounts. Too many to manage by hand, but we had no automation in place yet for features such as an account factory or a security baseline.

When I started they didn't have AWS Config set up. (Its setup was one of my tasks. We were on a tight budget though and every dollar hurt.)

I wasn't even sure whether CloudTrail was set up across all the accounts.

50 accounts was too many for me to check by hand. I could have done it, but I'm a lazy programmer. I would rather automate the task than grind through that by hand. Especially when I need to repeat the task again to check.

So what did I do? I wrote some Python!

From my notes:

> 2021-03-16. Starting to explore CloudTrail setup. Wrote a script to get all the CLI config for all the accounts in SSO. See generate_sso_config.bash

```
```

TODO: Review the code I wrote to check CloudTrail.

TAKEAWAY: Don't write this multithreaded code by yourself. It's tricky to get right.

Or ytou'll end up running into problems like this.

Make resources pickleable/serializable
https://github.com/boto/boto3/issues/678


To be fair, the docs before 2021 were unclear on how to write safe multithreaded code.

Add clarification on multithreading and multiprocessing for resources
https://github.com/boto/boto3/pull/2848

---

Later in the same year I won my biggest customer to date, Volkswagen. I joined the Basic Platform team providing account factory and security baseline services to the Digital Production Platform (DPP) and CFS organizations.

Across both production organizations we maintained about 1600 accounts. Even the INT org had over 100 accounts.

It was impossible to to do anything by hand across all accounts. Even a simple task became complicated by the need to repeat it 1600 times.

My janky approach that I got away with at Dentsu wasn't going to work here. I needed something better. I needed botocove.

This example runs in a single region and is still useful. All the trails were multi-region trails and one home region hosted them all.

Search notes for references to Botocove in VWAG repos.

```
ack -l "botocove" Personal/bitbucket/VWAG VWAG
```

I think this is the earliest use.

```
VWAG/codecommit/vulcan-res/trail-scripts/decommission-vwag-trail/README.md
VWAG/codecommit/vulcan-res/trail-scripts/decommission-vwag-trail/pyproject.toml
VWAG/codecommit/vulcan-res/trail-scripts/decommission-vwag-trail/poetry.lock
VWAG/codecommit/vulcan-res/trail-scripts/decommission-vwag-trail/check_trails.py
```

The main README shows how to collect inventory on AWS::CloudTrail::Trail resources.

This is still a great use case for botocove because not only does it show how to use the inventory feature but it shows how to use the remediation feature.

---

In April 2024 AWS offered 240 services [1]. CloudFormation by default supports almost 1200 resource types [2].

With so much choice and without proper management and governance, it's easy for a company's AWS accounts to grow complex and chaotic.

As a new organization administrator, you may be unsure whether someone is using any or all of the possible services and resource types.

---

# Botocove Quickstart

Run these commands in the `botocove_demo` folder.

Don't set the AWS environment first. The `.env` command breaks the venv command. (Can't reproduce this.)

Create a new virtualenv to interact with botocove.

```bash
python3 -m venv ./venv
source ./venv/bin/activate
pip install botocove ipython prettyprinter
```

Configure IPython with better pretty printing via a profile.

Start IPython and import botocove.

https://towardsdatascience.com/tips-ipython-d5ea85c5e9be?gi=7df368c1c91a

```bash
ipython \
--no-confirm-exit \
--no-banner \
--ipython-dir="$PWD" \
--InteractiveShellApp.extensions="['autoreload']" \
--InteractiveShellApp.exec_lines="['%autoreload 2', 'from botocove import cove', 'from boto3 import Session']"
```

```python
def simplify(obj):
    if isinstance(obj, dict) and obj.keys() == {
        "Results",
        "Exceptions",
        "FailedAssumeRole",
    }:
        return {k: [simplify(r) for r in v] for k, v in obj.items()}

    # Too lazy to write out all the keys.
    if isinstance(obj, dict) and {"Id", "RoleName", "RoleSessionName"} <= obj.keys():
        return {
            k: v
            for k, v in obj.items()
            if k in {"Id", "Name", "Region", "Result", "ExceptionDetails"}
        }

    return None
```

```python
@cove()
def hello_world(session):
    return "Hello, world!"

hellos = hello_world()
simplify(hellos)
```

Botocove equivalent of `aws cloudtrail describe-trails --query 'trailList'`.

```python
@cove()
def describe_trails(session):
    client = session.client("cloudtrail")
    return client.describe_trails()["trailList"]

trails = describe_trails()
```

Results like this:

```python
[
    {
        "HasCustomEventSelectors": False,
        "HasInsightSelectors": False,
        "HomeRegion": "eu-central-1",
        "IncludeGlobalServiceEvents": False,
        "IsMultiRegionTrail": False,
        "IsOrganizationTrail": False,
        "LogFileValidationEnabled": False,
        "Name": "AccountTrail-620591330564-eu-central-1",
        "S3BucketName": "cloudtrail-stack-set-trailbucket-xetebwwmth5w",
        "TrailARN": "arn:aws:cloudtrail:eu-central-1:620591330564:trail/AccountTrail-620591330564-eu-central-1",
    }
]
```

```python
@cove()
def get_trails_and_status(session):

    def iter_trail_statuses():
        client = session.client("cloudtrail")
        trail_list = client.describe_trails()["trailList"]

        for trail in trail_list:
            status = client.get_trail_status(Name=trail["Name"])
            yield {
                "Name": trail["Name"],
                "IsLogging": status["IsLogging"],
                "LoggingStarted": status["StartLoggingTime"].isoformat(),
                "LoggingStopped": status["StopLoggingTime"].isoformat(),
            }

    return list(iter_trail_statuses())


trails = get_trails_and_status()
```

Result like this:

```python
{'Name': 'AccountTrail-219424528675-eu-central-1', 'IsLogging': True}
```

```python
@cove()
def stop_logging(session):
    client = session.client("cloudtrail")
    trail_list = client.describe_trails()["trailList"]
    for trail in trail_list:
        client.stop_logging(Name=trail["Name"])
```

Results from `get_trails_and_status` like this:

```python
{
    'Name': 'AccountTrail-219424528675-eu-central-1',
    'IsLogging': False,
    'LoggingStarted': '2024-04-19T02:02:02.552000+02:00',
    'LoggingStopped': '2024-04-19T20:49:40.753000+02:00'
}
```

What abot the other regions?

Cove can take arguments for that.

Need to redefine the decorator function.

Or define the undecorated versions and don't use cove as a decorator (I do this in real life. Is it too complex for a first demo?)

Reconsider the need to show LoggingStarted and LoggingStopped. KISS.

## Write a script

Set up the trails for querying with Botocove. Logging is on by default.

```bash
rain deploy --yes cloudtrail_stack_set.yaml oldtrail1
rain deploy --yes cloudtrail_stack_set.yaml oldtrail2
```

Set the trails to stop logging via CloudFormation.

```bash
rain deploy --yes cloudtrail_stack_set.yaml oldtrail1 --params IsLogging=False
rain deploy --yes cloudtrail_stack_set.yaml oldtrail2 --params IsLogging=False
```

Tear down the trails.

```bash
rain rm --yes oldtrail1
rain rm --yes oldtrail2
```

Write a source script called `set_up_demo_env`. It sets up the demo environment.

Start the shell for the Sandbox.

```bash
.env aws-sandbox-b
```

Set up the demo env.

```bash
source set_up_demo_env
```

Start the IPython botocove shell.

```bash
ipy
```

```python
hello = hello_world()

descriptions = describe_account_trails()

descriptions = describe_account_trails_in_more_regions()

old_statuses = get_logging_status()

stops = stop_logging()

new_statuses = get_trails_and_status()

# Then again for multi-region.

# Then again for starting the trails again in an OU.

# Then aws-org-tree.
```

---


## Press

AWS Summit London April 24th, EXCEL London

If you are heading to the AWS Summit London then make sure you head over to the open source demo booth over in the AWS for Every App village. We have nine hand selected demos across a broad range of technologies, I whilst I cannot be there myself, I am super excited about this. Find out more about the demos, and the schedule by checking out the post I put together, Open Source demos at AWS Summit London

https://community.aws/content/2ea38u0x4DZ91l6BO2CoWHPo7rw/aws-open-source-newsletter-195

Botocove and aws-org-tree - 1:15pm

This demo slot will walk you through two different open source projects.

Botocove, originally created by Dave Connell and now maintained by AWS Community Builder Iain Elder, allows you to run a Python function against a selection of AWS accounts, Organizational Units (OUs) or all AWS accounts in an organization, concurrently with thread safety. Run in one or multiple regions.

aws-org-tree, created by Iain, is a handy command line tool that prints a text tree representation of an AWS organization (think tree command)

https://github.com/connelldave/botocove and https://github.com/iainelder/aws-org-tree

https://community.aws/content/2dXeKqSAbqVYrbPMnKT9zQ6BaVU/open-source-demos-at-the-aws-summit-london

[1]: Overview of Amazon Web Services AWS Whitepaper. Accessed 2024-04-17.
[2]: `aws cloudformation list-types --visibility PUBLIC --type RESOURCE --filters Category=AWS_TYPES --query 'TypeSummaries | length(@)'`. Executed 2024-04-17. Returned 1188.

---

Learn how to use speaker notes with Andy Haskell.

https://dev.to/andyhaskell/write-your-tech-talk-slides-rapidly-with-marp-2c7g

Google `"cloudtrail" second trail cost explorer`

https://medium.com/airbnb-engineering/achieving-insights-and-savings-with-cost-data-ec9a49fd74bc

https://www.nops.io/blog/aws-cost-optimization-tool-find-untagged-aws-resources/

Legend of the Boto Core-de-Rosa
https://thenib.com/legend-of-the-boto-cor-de-rosa/
