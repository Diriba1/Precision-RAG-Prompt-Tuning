from django.db import models

# Create your models here.

class PromptGen(models.Model):
    description = models.TextField()
    test_cases = models.TextField()
    number_of_prompts = models.IntegerField(default=10)
    use_wandb = models.BooleanField(default=False)

class Prompt(models.Model):
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class Evaluation(models.Model):
    prompt1 = models.ForeignKey(Prompt, on_delete=models.CASCADE, related_name='evaluations_as_first')
    prompt2 = models.ForeignKey(Prompt, on_delete=models.CASCADE, related_name='evaluations_as_second')
    winner = models.ForeignKey(Prompt, on_delete=models.CASCADE, related_name='evaluations_won', null=True)
    created_at = models.DateTimeField(auto_now_add=True)

class Rating(models.Model):
    prompt = models.ForeignKey(Prompt, on_delete=models.CASCADE)
    elo_rating = models.IntegerField(default=1500)

