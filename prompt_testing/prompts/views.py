from .models import *
from .forms import PromptForm
from django.shortcuts import render, redirect
from .utils import generate_optimal_prompt

# Create your views here.
def prompt_list(request):
    prompts = Prompt.objects.all().order_by('-created_at')  # Fetch prompts ordered by creation time
    context = {'prompts': prompts}
    return render(request, 'prompts/list.html', context)

# Create a PromptForm class (if not already defined) to validate the prompt text.
# In the view, check if the request is a POST request and handle form submission.
# Use the form data to create a new Prompt object and save it to the database.
# You can then either trigger a matchup immediately or store the prompt for later use.


def prompt_create(request):
    if request.method == 'POST':
        form = PromptForm(request.POST)
        if form.is_valid():
            prompt = form.save()
            # Trigger matchup or store prompt for later
            # ...
            return redirect('prompt_list')
    else:
        form = PromptForm()

    context = {'form': form}
    return render(request, 'prompts/create.html', context)


# This view handles GET requests from the form in matchup.html.
# It retrieves the selected prompt IDs, fetches the corresponding Prompt objects, and triggers the trigger_matchup function to perform the matchup logic and generate results.
# It updates ELO ratings and stores the results in the database and Pinecone.
# Finally, it prepares data for the template to display the matchup results.

def prompt_matchup(request, pk):
    try:
        prompt1 = Prompt.objects.get(pk=pk)
    except Prompt.DoesNotExist:
        raise Http404("Prompt does not exist")

    # Get second prompt (replace with your selection logic)
    prompt2 = Prompt.objects.filter(pk__gt=pk).order_by('?').first()  # Randomly select a prompt with a higher PK

    # Run matchup logic (replace with your LLM interaction and evaluation)
    winner_prompt = prompt1  # Placeholder for LLM-based winner determination

    # Update ELO ratings
    update_elo_ratings(prompt1, prompt2, winner_prompt)

    # Render results
    context = {
        'prompt1': prompt1,
        'prompt2': prompt2,
        'winner_prompt': winner_prompt,
    }
    return render(request, 'prompts/matchup.html', context)

# Implement trigger_matchup, update_elo_ratings, and store_results functions
# Helper function for ELO rating updates

# K-Factor: Determines the magnitude of rating changes. Adjusted based on desired sensitivity.
# Expected Scores: Calculate the expected scores for each prompt based on their current ratings.
# New Ratings: Update the ratings based on the actual outcome (1 for the winner, 0 for the loser) and the K-factor.

def update_elo_ratings(prompt1, prompt2, winner_prompt):
    K = 32  # Adjust K-factor as needed (e.g., lower for more established prompts)
    default_elo = 1500  # Example default rating

    prompt1.elo_rating = prompt1.elo_rating if hasattr(prompt1, 'elo_rating') else default_elo
    prompt2.elo_rating = prompt2.elo_rating if hasattr(prompt2, 'elo_rating') else default_elo

    expected_score1 = 1 / (1 + 10**((prompt2.elo_rating - prompt1.elo_rating) / 400))
    expected_score2 = 1 - expected_score1

    new_rating1 = prompt1.elo_rating + K * (1 - expected_score1)
    new_rating2 = prompt2.elo_rating + K * (0 - expected_score2)

    prompt1.elo_rating = new_rating1
    prompt2.elo_rating = new_rating2

    prompt1.save()
    prompt2.save() 



def home_view(request):
    prompts = PromptGen.objects.all()
    return render(request, "prompts/home.html", {"prompts": prompts})

def generate_prompt_view(request):
    if request.method == 'POST':
        description = request.POST.get("description", "")
        test_cases = request.POST.get("test_cases", "")
        number_of_prompts = int(request.POST.get("number_of_prompts", 10))
        use_wandb = bool(request.POST.get("use_wandb", False))

        # Save the prompt to the database
        prompt = PromptGen.objects.create(
            description=description,
            test_cases=test_cases,
            number_of_prompts=number_of_prompts,
            use_wandb=use_wandb
        )

        # Call the function to generate and test prompts
        result = generate_optimal_prompt(description, test_cases, number_of_prompts, use_wandb)

        # Update the result in the database
        prompt.result = result
        prompt.save()

        return redirect('home')




