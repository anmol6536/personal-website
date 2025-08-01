from markdown import markdown

# Dummy Data for the entire application

events = [
    {
        "title": "Platform Engineer, Viome Life Sciences",
        "date": "Jan 2025 - Present",
        "icon": "cloud_queue",
        "blurb": "Developing Viome's platform with a focus on complex scoring engines. Proficient in Azure, AWS, distributed cloud compute, and algorithm optimization.",
        "skills": ["Azure", "AWS", "Distributed Systems", "Algorithm Optimization", "Python"]
    },
    {
        "title": "Scientist, Viome Life Sciences",
        "date": "May 2022 - Jan 2025",
        "icon": "biotech",
        "blurb": "Building ML tools and scalable platforms for biological data. Developed and integrated over 60 production models and their APIs.",
        "skills": ["Machine Learning", "API Development", "Python", "Scalable Platforms"]
    },
    {
        "title": "Research Scientist, GeneCentrix",
        "date": "Jan 2020 - May 2022",
        "icon": "biotech",
        "blurb": "Led a project with Abbvie, developed a high-throughput molecular docking platform, and created a Python package that improved algorithm speed by over 1000x.",
        "skills": ["Molecular Docking", "Python", "High-Throughput Screening", "Drug Discovery"]
    },
    {
        "title": "M.S. in Biotechnology, NYU",
        "date": "Aug 2020 - May 2022",
        "icon": "school",
        "blurb": "Focused on the intersection of biology and technology at New York University.",
        "skills": ["Biotechnology", "Genomics", "Data Analysis"]
    },
    {
        "title": "M.S. in Biotechnology, VIT",
        "date": "June 2015 - May 2017",
        "icon": "school",
        "blurb": "Completed my Master's degree at Vellore Institute of Technology.",
        "skills": ["Biotechnology", "Research"]
    },
    {
        "title": "B.S. in Microbiology & Biochemistry",
        "date": "June 2012 - May 2015",
        "icon": "school",
        "blurb": "Laid my scientific foundations at St. Xavier's University, Mumbai.",
        "skills": ["Microbiology", "Biochemistry", "Lab Techniques"]
    }
]

publications = [
    {
        "title": "Altered gut microbial functional pathways in people with Irritable Bowel Syndrome enable precision health insights",
        "authors": "Eric Patridge, Anmol Gorakshakar, Matthew M. Molusky, Oyetunji Ogundijo, Angel Janevski, Cristina Julian, Lan Hu, Momchilo Vuyisich, and Guruduth Banavar",
        "journal": "BMC Gastroenterology (2025)",
        "url": "#",
        "year": "2025"
    },
    {
        "title": "Microbial functional pathways based on metatranscriptomic profiling enable effective saliva-based health assessments for precision wellness.",
        "authors": "Patridge, E., Gorakshakar, A., Molusky, M. M., et al.",
        "journal": "bioRxiv (2023)",
        "url": "https://www.biorxiv.org/content/10.1101/2023.11.16.567433v1",
        "year": "2023"
    },
    {
        "title": "The effectiveness of precision supplements on depression symptoms in a US population.",
        "authors": "Julian, C., Shen, N., Molusky, M., Gopu, V., Gorakshakar, A., et al.",
        "journal": "medRxiv (2023)",
        "url": "https://www.medrxiv.org/content/10.1101/2023.04.14.23288594v1",
        "year": "2023"
    },
    {
        "title": "TOR kinase activity in Chlamydomonas reinhardtii is modulated by cellular metabolic states.",
        "authors": "Upadhyaya, S., Agrawal, S., Gorakshakar, A., & Rao, B. J.",
        "journal": "FEBS letters (2020)",
        "url": "https://febs.onlinelibrary.wiley.com/doi/full/10.1002/1873-3468.13902",
        "year": "2020"
    }
]

projects = [
    {
        "title": "microservices",
        "description": "A collection of microservices demonstrating various patterns and practices.",
        "url": "https://github.com/anmol6536/microservices",
        "tech": ["Python", "Flask", "Docker"]
    },
    {
        "title": "htmx-py",
        "description": "A fast, clean htmx-centric development template to render HTML components directly from Python.",
        "url": "https://github.com/anmol6536/htmx-py",
        "tech": ["Python", "HTMX", "Flask"]
    }
]

photos = [
    {"id": 1, "slug": "tokyo-streets", "url": "https://images.unsplash.com/photo-1542051841857-5f90071e7989?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=2070&q=80", "caption": "Neon-lit night in Shinjuku, Tokyo."},
    {"id": 2, "slug": "italian-coast", "url": "https://images.unsplash.com/photo-1516483638261-f4dbaf036963?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1974&q=80", "caption": "Pastel houses of the Amalfi Coast."},
    {"id": 3, "slug": "forest-path", "url": "https://images.unsplash.com/photo-1441974231531-c6227db76b6e?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=2071&q=80", "caption": "A quiet walk in a misty forest."},
    {"id": 4, "slug": "sourdough-creation", "url": "https://images.unsplash.com/photo-1589467941019-b5722c24476c?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1974&q=80", "caption": "The perfect sourdough crumb."},
    {"id": 5, "slug": "urban-lines", "url": "https://images.unsplash.com/photo-1506929562872-bb421503ef21?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=2070&q=80", "caption": "Architectural lines in a modern city."},
    {"id": 6, "slug": "morning-coffee", "url": "https://images.unsplash.com/photo-1497935586351-b67a49e012bf?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=2071&q=80", "caption": "A slow morning with a good cup of coffee."}
]

dev_posts = [
    {
        "slug": "understanding-async-python",
        "title": "Understanding Asyncio in Python",
        "date": "November 5, 2023",
        "author": "Anmol Gorakshakar",
        "content": markdown("A deep dive into Python's asyncio library. We'll explore coroutines, event loops, and how to write efficient, concurrent code."),
        "related": ["docker-for-local-development"]
    },
    {
        "slug": "docker-for-local-development",
        "title": "Docker for Local Development",
        "date": "October 18, 2023",
        "author": "Anmol Gorakshakar",
        "content": markdown("Learn how to streamline your local development environment using Docker. This guide covers creating Dockerfiles, using docker-compose, and managing containers."),
        "related": ["understanding-async-python"]
    }
]

recipes = [
    {
        "slug": "classic-spaghetti-carbonara",
        "title": "Classic Spaghetti Carbonara",
        "description": "A traditional Italian pasta dish from Rome made with eggs, hard cheese, cured pork, and black pepper.",
        "image_url": "https://images.unsplash.com/photo-1588013273468-411962b21955?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=2070&q=80",
        "servings": 4,
        "prep_time": "10 minutes",
        "cook_time": "15 minutes",
        "calories_per_serving": 650,
        "category": "Main Course",
        "cuisine": "Italian",
        "ingredients": [
            {"name": "Spaghetti", "amount": 400, "unit": "g"},
            {"name": "Guanciale or Pancetta, diced", "amount": 150, "unit": "g"},
            {"name": "Large Egg Yolks", "amount": 4, "unit": ""},
            {"name": "Pecorino Romano Cheese, freshly grated", "amount": 50, "unit": "g"},
            {"name": "Black Pepper, freshly ground", "amount": 1, "unit": "tsp"},
        ],
        "instructions": [
            "Bring a large pot of salted water to a boil. Cook the spaghetti according to package directions until al dente.",
            "While the pasta is cooking, heat a large skillet over medium heat. Add the guanciale and cook until it is crispy and the fat has rendered, about 5-7 minutes. Remove from heat.",
            "In a medium bowl, whisk together the egg yolks and Pecorino Romano cheese. Season generously with black pepper.",
            "Just before the pasta is done, reserve about 1 cup of the pasta water. Drain the pasta and immediately add it to the skillet with the guanciale. Toss to combine.",
            "Pour the egg and cheese mixture over the pasta, stirring quickly to create a creamy sauce. If the sauce is too thick, add a tablespoon or two of the reserved pasta water. The heat of the pasta will cook the eggs.",
            "Serve immediately, with extra grated cheese and black pepper on top."
        ]
    },
    {
        "slug": "creamy-tomato-risotto",
        "title": "Creamy Tomato Risotto",
        "description": "A comforting and flavorful risotto made with rich tomatoes and creamy Arborio rice.",
        "image_url": "https://images.unsplash.com/photo-1595908129742-8781ba8b4226?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1974&q=80",
        "servings": 2,
        "prep_time": "15 minutes",
        "cook_time": "30 minutes",
        "calories_per_serving": 450,
        "category": "Main Course",
        "cuisine": "Italian",
        "ingredients": [
            {"name": "Arborio Rice", "amount": 200, "unit": "g"},
            {"name": "Vegetable Broth, warm", "amount": 1, "unit": "L"},
            {"name": "Canned Crushed Tomatoes", "amount": 400, "unit": "g"},
            {"name": "Yellow Onion, finely chopped", "amount": 1, "unit": ""},
            {"name": "Garlic, minced", "amount": 2, "unit": "cloves"},
            {"name": "Dry White Wine", "amount": 60, "unit": "ml"},
            {"name": "Parmesan Cheese, grated", "amount": 50, "unit": "g"},
            {"name": "Butter", "amount": 2, "unit": "tbsp"},
            {"name": "Olive Oil", "amount": 1, "unit": "tbsp"},
            {"name": "Fresh Basil, for garnish", "amount": 1, "unit": "handful"}
        ],
        "instructions": [
            "In a large saucepan or Dutch oven, heat the olive oil and 1 tablespoon of butter over medium heat. Add the chopped onion and cook until softened, about 5 minutes.",
            "Add the garlic and cook for another minute until fragrant. Add the Arborio rice and toast for 1-2 minutes, stirring constantly, until the grains are translucent at the edges.",
            "Pour in the white wine and cook until it has been completely absorbed by the rice.",
            "Begin adding the warm vegetable broth one ladleful at a time, waiting for the liquid to be mostly absorbed before adding the next. Stir frequently.",
            "After about 10 minutes, stir in the crushed tomatoes. Continue adding broth and stirring until the rice is creamy and al dente, about 15-20 minutes total.",
            "Remove the risotto from the heat. Stir in the remaining tablespoon of butter and the grated Parmesan cheese. Season with salt and pepper to taste.",
            "Serve immediately, garnished with fresh basil."
        ]
    }
] 