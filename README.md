This devops-lab fratures a simple server app handling basic get requests.

So far we've created a docker image to run the app that Kubernetes can then take and make into a cluster. We've also created a test suite in python.

Next, we're going to implement Github actions to use our test suite and thentie in Argo CD to reconcile Kubernetes manifests.

At least, thats how I understand it! I haven't done as much CI/CD work so this is mostly just me getting my feet wet.
