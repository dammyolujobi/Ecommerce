# SET UP FOR GOOGLE AUTH(google.auth.default())

- Download and set up the Google Cloud CLI installer

```Powershell
(New-Object Net.WebClient).DownloadFile("https://dl.google.com/dl/cloudsdk/channels/rapid/GoogleCloudSDKInstaller.exe", "$env:Temp\GoogleCloudSDKInstaller.exe")

& $env:Temp\GoogleCloudSDKInstaller.exe

```

- For more info visit [website](https://cloud.google.com/docs/authentication/set-up-adc-local-dev-environment)  

- For local shell create a local authentication credential for your user account:

```bash
    gcloud auth application-default login
```

-Get the location of your credentials and put in your project environment
