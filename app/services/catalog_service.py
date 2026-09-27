from urllib.parse import quote_plus


PLATFORMS = {

    "Amazon":
        "https://www.amazon.in/s?k={q}",

    "Flipkart":
        "https://www.flipkart.com/search?q={q}",

    "IKEA":
        "https://www.ikea.com/in/en/search/?q={q}",

    "Swiggy":
        "https://www.swiggy.com/search?query={q}",

    "Zomato":
        "https://www.zomato.com/search?q={q}",

    "OYO":
        "https://www.oyorooms.com/search?location={q}",
}


def search_url(
    platform: str,
    query: str
) -> str:

    template = PLATFORMS.get(
        platform,
        PLATFORMS["Amazon"]
    )

    return template.format(
        q=quote_plus(query)
    )


def home_catalog(
    style: str,
    items: list[dict]
) -> list[dict]:

    defaults = [

        (
            "LED ceiling light",
            "Lighting",
            1800,
            "Amazon"
        ),

        (
            "5-star ceiling fan",
            "Fans",
            3200,
            "Flipkart"
        ),

        (
            "Compact dining table",
            "Dining",
            8500,
            "IKEA"
        ),

        (
            "Accent wall art",
            "Decor",
            2200,
            "Amazon"
        ),

        (
            "Storage cabinet",
            "Storage",
            6500,
            "IKEA"
        ),

        (
            "Modern sofa",
            "Furniture",
            18000,
            "Flipkart"
        ),
    ]

    requested = {
        item["category"].lower():
            item["quantity"]

        for item in items
    }

    result = []

    for (
        name,
        category,
        price,
        platform
    ) in defaults:

        matching_keys = [
            key
            for key in requested
            if (
                category.lower() in key
                or key in category.lower()
            )
        ]

        if matching_keys:

            quantity = requested[
                matching_keys[0]
            ]

            result.append({

                "name":
                    f"{style.title()} {name}",

                "category":
                    category,

                "estimated_price":
                    price,

                "quantity":
                    quantity,

                "platform":
                    platform,

                "url":
                    search_url(
                        platform,
                        f"{style} {name}"
                    ),
            })

    if not result:

        for (
            name,
            category,
            price,
            platform
        ) in defaults[:4]:

            result.append({

                "name":
                    f"{style.title()} {name}",

                "category":
                    category,

                "estimated_price":
                    price,

                "quantity":
                    1,

                "platform":
                    platform,

                "url":
                    search_url(
                        platform,
                        f"{style} {name}"
                    ),
            })

    return result


def party_catalog(
    event_type: str,
    city: str
) -> list[dict]:

    return [

        {
            "name":
                f"{event_type.title()} catering search",

            "category":
                "Catering",

            "estimated_price":
                350 * 10,

            "quantity":
                1,

            "platform":
                "Zomato",

            "url":
                search_url(
                    "Zomato",
                    f"{event_type} catering {city}"
                ),
        },

        {
            "name":
                f"{event_type.title()} food delivery options",

            "category":
                "Food",

            "estimated_price":
                250 * 10,

            "quantity":
                1,

            "platform":
                "Swiggy",

            "url":
                search_url(
                    "Swiggy",
                    f"{event_type} food {city}"
                ),
        },

        {
            "name":
                f"{city} event venue search",

            "category":
                "Venue",

            "estimated_price":
                12000,

            "quantity":
                1,

            "platform":
                "OYO",

            "url":
                search_url(
                    "OYO",
                    f"{event_type} venue {city}"
                ),
        },

        {
            "name":
                f"{event_type.title()} decoration ideas",

            "category":
                "Decoration",

            "estimated_price":
                5000,

            "quantity":
                1,

            "platform":
                "Amazon",

            "url":
                search_url(
                    "Amazon",
                    f"{event_type} party decoration"
                ),
        },
    ]


def jewelry_catalog(
    style: str,
    occasion: str,
    metal: str | None
) -> list[dict]:

    metal_text = (
        f" {metal}"
        if metal
        else ""
    )

    queries = [

        (
            f"{style}{metal_text} earrings for {occasion}",
            "Earrings",
            999
        ),

        (
            f"{style}{metal_text} necklace for {occasion}",
            "Necklace",
            1799
        ),

        (
            f"{style}{metal_text} bracelet for {occasion}",
            "Bracelet",
            899
        ),

        (
            f"{style}{metal_text} jewelry set for {occasion}",
            "Jewelry Set",
            2499
        ),
    ]

    result = []

    for index, (
        query,
        category,
        price
    ) in enumerate(queries):

        platform = (
            "Amazon"
            if index % 2 == 0
            else "Flipkart"
        )

        result.append({

            "name":
                query.title(),

            "category":
                category,

            "estimated_price":
                price,

            "quantity":
                1,

            "platform":
                platform,

            "url":
                search_url(
                    platform,
                    query
                ),
        })

    return result