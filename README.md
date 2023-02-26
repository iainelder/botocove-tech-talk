# Botocove Tech Talk Draft

See [fwd:cloudsec Call for Papers](fwdcloudsec_cfp.md) for the motivation.

> Our main theme for this year is “Blurring Lines.” We’re especially interested in talks that show how we’re navigating the changing boundaries in our cloud environments -- and the evolution in “shared responsibility” as a result. We’re also looking for other creative ideas on how we can facilitate discussion and solve problems together as the cloud security community.

TODO: See full CFP text on website.

## Shared responsibility for inventory

AWS's Config a configuration management database as a service.

AWS records the configuration for some, but not all resources.

The recording is not automatic. It's something you have to configure explicitly in each account and region.

A sample CloudFormation stack set is provided in the documentation. You may need to modify it to meet your local standards.

AWS Config provides hooks to perform actions on recorded changes to configuration.

Hooks can be distributed as organization conformance packs. Basically a CloudFormation stack set with a different API (and frustratingly different semantics around failures).

Setting up AWS config and the remediation hooks is a lot of up-front work. Depending on the bureaucracy of your environment, this may make it difficult to use this service to its fullest potential.

Even when AWS Config is up and running, its coverage gaps mean that it can't be used to inventorize all resources or even meet all use cases of those it does support (IsLogging CloudTrail was the first thing I used Botocove for).

## Botocove architecture diagram

Draw one using PlantUML.

## Botocove use cases

* One inventorizing use case
* One remediating use case

## Pros and cons

* +: Minimal setup inside the AWS account. As long as you have enough permissions in the accounts you can use it.
* +: Because it runs arbitrary Python functions, you can do anything boto3 can
* -: Because it runs arbitrary Python functions, you have to write a lot of code to do stuff
* -: Including development time, it's about 100 to 1000 times slower than querying using AWS Config
* -: It runs on your local machine, so limited by its resources

## Competitors

* CloudQuery
* Steampipe
* Remo
