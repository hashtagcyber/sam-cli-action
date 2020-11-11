# @hashtagcyber/sam-cli-action
Fork of @TractorZoom/sam-cli-action
- Stripped out Node/Go
- Using a different container
- Added a python script to guess what the right build directory is


Github action for using the [AWS SAM CLI](https://github.com/awslabs/aws-sam-cli) to build and deploy serverless applications. (Python)
### Getting Started:

1. Add `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, and `AWS_DEFAULT_REGION` in Settings > Secrets.

2. Create a workflow file with a yaml config like the one below (.github/workflows/build-and-test.yaml)
- You probably don't want random actions owned by a random person having access to your AWS keys
    - That's a hint that you should fork this action ;)
- This config will run sam build and sam deploy --no-execute-changeset on every PR to the repo.
- The output will be attached as a comment to the PR
- You MUST have samconfig.toml included in git
- This action assumes that each project is located in a folder named 'sam-{project name}'. Modify find-project.py if you want to use a different prefix
- Each PR may only update ONE sam project.

```yaml
name: Build and Test
on:
  pull_request:
    branches: [ main ]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: sam build
        uses: hashtagcyber/sam-cli-action@master
        with:
          sam_command: "build"
        env:
          AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}
          AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          AWS_DEFAULT_REGION: ${{ secrets.AWS_DEFAULT_REGION }} 
          GITHUB_TOKEN: ${{secrets.GITHUB_TOKEN }}
      - name: sam test
        uses: hashtagcyber/sam-cli-action@master
        with:
          sam_command: "deploy --no-execute-changeset --no-fail-on-empty-changeset"
          actions_comment: true
        env:
          AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}
          AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          AWS_DEFAULT_REGION: ${{ secrets.AWS_DEFAULT_REGION }}
          GITHUB_TOKEN: ${{secrets.GITHUB_TOKEN }}

```

3. If you want to auto-deploy on merge... just add another config (.github/workflows/deploy.yaml)
- Don't use this to run your startup, there aren't any guardrails/alarming for when the deploy fails.

```yaml
ame: Build and Deploy
on:
  push:
    branches: [ main ]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: sam build
        uses: hashtagcyber/sam-cli-action@master
        with:
          sam_command: "build"
        env:
          AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}
          AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          AWS_DEFAULT_REGION: ${{ secrets.AWS_DEFAULT_REGION }} 
          GITHUB_TOKEN: ${{secrets.GITHUB_TOKEN }}
      - name: sam deploy
        uses: hashtagcyber/sam-cli-action@master
        with:
          sam_command: "deploy --no-fail-on-empty-changeset"
          actions_comment: true
        env:
          AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}
          AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          AWS_DEFAULT_REGION: ${{ secrets.AWS_DEFAULT_REGION }}
          GITHUB_TOKEN: ${{secrets.GITHUB_TOKEN }}
```
4. For SAM Projects that are already deployed; magic happens and updates should be pushed automatically to your AWS environment. For new projects (IE, you're about to run sam init), I usually execute the following:
- sam init
    - Don't forget, sam-blah
- <codey codey code>
- sam build
- sam deploy --guided
    - No, don't prompt me for changes; yes, please save my settings in samconfig.toml
- <Whirring of steam, your cloudformation gets deployed>
- git add .
    - Yes, terrible, but just make sure the project folder and samconfig.toml are added to your commit
- git commit -m 'I'm awesome, first post, but this is already running in production'
- git push
- <clicky click in the UI, merge to main>
- At this point, any future updates to the infra can be submitted via PR. Pushes to main will get deployed... YAAAAAYYYYY
