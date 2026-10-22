
from pyscript import document, when
from datetime import date
import json


haircuts = [
    {
        "id": 1,
        "name": "Low Fade",
        "category": "Fade",
        "price": 150,
        "description": "A clean, subtle fade around the ears and neckline.",
        "image": "lowfade.jpeg"
    },
    {
        "id": 2,
        "name": "Mid Fade",
        "category": "Fade",
        "price": 180,
        "description": "A balanced fade that gives you a fresh, sharp look.",
        "image": "midfade.webp"
    },
    {
        "id": 3,
        "name": "High Fade",
        "category": "Fade",
        "price": 200,
        "description": "A bold, high-contrast fade for a confident style.",
        "image": "highfade.jpeg"
    },
    {
        "id": 4,
        "name": "Buzz Cut",
        "category": "Classic",
        "price": 100,
        "description": "A simple, low-maintenance cut with an even finish.",
        "image": "buzzcut.jpeg"
    },
    {
        "id": 5,
        "name": "Crew Cut",
        "category": "Classic",
        "price": 120,
        "description": "A timeless short hairstyle that looks neat and clean.",
        "image": "crewcut.jpeg"
    },
    {
        "id": 6,
        "name": "Classic Side Part",
        "category": "Classic",
        "price": 150,
        "description": "A polished side-parted hairstyle for any occasion.",
        "image": "classicsidepart.jpeg"
    },
    {
        "id": 7,
        "name": "Textured Crop",
        "category": "Modern",
        "price": 180,
        "description": "A textured top with a stylish, modern finish.",
        "image": "texturedcrop.jpeg"
    },
    {
        "id": 8,
        "name": "Two Block",
        "category": "Modern",
        "price": 220,
        "description": "A trendy layered look with a longer top section.",
        "image": "twoblock.jpg"
    },
    {
        "id": 9,
        "name": "Pompadour",
        "category": "Modern",
        "price": 250,
        "description": "A voluminous top with a smooth, stylish finish.",
        "image": "pompadour.jpeg"
    },
    {
        "id": 10,
        "name": "Skin Fade",
        "category": "Fade",
        "price": 220,
        "description": "A sharp skin-level fade with a clean gradient.",
        "image": "skinfade.webp"
    }
]

selected_category = "All"
selected_haircut = None




def get_element(element_id):
    return document.getElementById(element_id)


def money(amount):
    return f"₱{amount:,.2f}"


def find_haircut(haircut_id):
    for haircut in haircuts:
        if haircut["id"] == haircut_id:
            return haircut
    return None




def render_haircuts():
    grid = get_element("haircutGrid")
    search_text = get_element("searchInput").value.lower().strip()

    grid.innerHTML = ""

    filtered = []

    for haircut in haircuts:
        matches_category = (
            selected_category == "All"
            or haircut["category"] == selected_category
        )

        matches_search = (
            search_text in haircut["name"].lower()
            or search_text in haircut["description"].lower()
            or search_text in haircut["category"].lower()
        )

        if matches_category and matches_search:
            filtered.append(haircut)

    if not filtered:
        grid.innerHTML = """
            <p class="loading">
                No haircuts found. Try another search or category.
            </p>
        """
    else:
        for haircut in filtered:
            card = document.createElement("article")
            card.className = "haircut-card"

            # Build the card with escaped text values.
            safe_name = (
                haircut["name"].replace("&", "&amp;")
                .replace("<", "&lt;").replace(">", "&gt;")
                .replace('"', "&quot;").replace("'", "&#x27;")
            )
            safe_description = (
                haircut["description"].replace("&", "&amp;")
                .replace("<", "&lt;").replace(">", "&gt;")
                .replace('"', "&quot;").replace("'", "&#x27;")
            )
            safe_category = (
                haircut["category"].replace("&", "&amp;")
                .replace("<", "&lt;").replace(">", "&gt;")
            )

            card.innerHTML = f"""
                <img
                    src="{haircut['image']}"
                    alt="{safe_name} haircut"
                    loading="lazy"
                    onerror="this.style.display='none'">

                <div class="card-content">
                    <div class="card-top">
                        <h3>{safe_name}</h3>
                        <span class="category-tag">{safe_category}</span>
                    </div>

                    <p class="card-description">
                        {safe_description}
                    </p>

                    <div class="card-bottom">
                        <span class="price">{money(haircut['price'])}</span>

                        <button
                            class="book-card"
                            type="button"
                            data-haircut-id="{haircut['id']}">
                            Choose Style
                        </button>
                    </div>
                </div>
            """

            grid.appendChild(card)

    get_element("resultsCount").innerText = (
        f"Showing {len(filtered)} of {len(haircuts)} haircut styles"
    )




def populate_haircut_dropdown():
    dropdown = get_element("haircutSelect")

    dropdown.innerHTML = '<option value="">Select a haircut</option>'

    for haircut in haircuts:
        option = document.createElement("option")
        option.value = str(haircut["id"])
        option.text = (
            f"{haircut['name']} - {money(haircut['price'])}"
        )
        dropdown.appendChild(option)




def update_price():
    selected_value = get_element("haircutSelect").value
    price_display = get_element("estimatedPrice")

    if not selected_value:
        price_display.innerText = money(0)
        return

    try:
        haircut_id = int(selected_value)
    except (ValueError, TypeError):
        price_display.innerText = money(0)
        return

    haircut = find_haircut(haircut_id)

    if haircut:
        price_display.innerText = money(haircut["price"])
    else:
        price_display.innerText = money(0)



@when("click", "#haircutGrid")
def choose_haircut(event):
    button = event.target.closest(".book-card")

    if button is None:
        return

    try:
        haircut_id = int(button.getAttribute("data-haircut-id"))
    except (ValueError, TypeError):
        return

    haircut = find_haircut(haircut_id)

    if haircut:
        get_element("haircutSelect").value = str(haircut_id)
        update_price()

        # Scroll to the booking form.
        get_element("booking").scrollIntoView(
            {"behavior": "smooth", "block": "start"}
        )



@when("input", "#searchInput")
def search_haircuts(event):
    render_haircuts()



@when("click", "#categoryFilters")
def filter_haircuts(event):
    global selected_category

    button = event.target.closest(".filter")

    if button is None:
        return

    selected_category = button.getAttribute("data-category")

    filters = document.querySelectorAll(".filter")

    for filter_button in filters:
        filter_button.classList.remove("active")

    button.classList.add("active")

    render_haircuts()



@when("change", "#haircutSelect")
def haircut_changed(event):
    update_price()



@when("submit", "#bookingForm")
def submit_booking(event):
    event.preventDefault()

    message = get_element("bookingMessage")
    message.className = "booking-message"

    name = get_element("customerName").value.strip()
    phone = get_element("customerPhone").value.strip()
    selected_value = get_element("haircutSelect").value
    booking_date = get_element("bookingDate").value
    booking_time = get_element("bookingTime").value

    # Check required values.
    if not name or not phone or not selected_value:
        message.classList.add("error")
        message.innerText = "Please complete all required fields."
        return

    if not booking_date or not booking_time:
        message.classList.add("error")
        message.innerText = "Please select your preferred date and time."
        return

    # Validate the date.
    try:
        chosen_date = date.fromisoformat(booking_date)

        if chosen_date < date.today():
            message.classList.add("error")
            message.innerText = "Please choose today or a future date."
            return
    except ValueError:
        message.classList.add("error")
        message.innerText = "Please enter a valid appointment date."
        return

    # Basic phone number validation.
    cleaned_phone = phone.replace(" ", "").replace("-", "")

    if not cleaned_phone.isdigit() or len(cleaned_phone) < 7:
        message.classList.add("error")
        message.innerText = "Please enter a valid phone number."
        return

    try:
        haircut_id = int(selected_value)
    except (ValueError, TypeError):
        message.classList.add("error")
        message.innerText = "Please choose a valid haircut."
        return

    haircut = find_haircut(haircut_id)

    if haircut is None:
        message.classList.add("error")
        message.innerText = "That haircut could not be found."
        return

    # Convert the selected time to a readable format.
    hour, minute = map(int, booking_time.split(":"))
    period = "AM" if hour < 12 else "PM"
    display_hour = hour % 12 or 12
    display_time = f"{display_hour}:{minute:02d} {period}"

    # Display the booking request summary.
    safe_name = (
        name.replace("&", "&amp;")
        .replace("<", "&lt;").replace(">", "&gt;")
    )
    safe_haircut_name = (
        haircut["name"].replace("&", "&amp;")
        .replace("<", "&lt;").replace(">", "&gt;")
    )

    message.classList.add("success")
    message.innerHTML = f"""
        <strong>Booking request created!</strong><br><br>
        Customer: {safe_name}<br>
        Haircut: {safe_haircut_name}<br>
        Price: {money(haircut['price'])}<br>
        Date: {booking_date}<br>
        Time: {display_time}<br><br>
        <strong>Important:</strong> This is a local demo request.
        Your appointment is not confirmed until the barbershop
        confirms it.
    """


get_element("bookingDate").min = date.today().isoformat()


populate_haircut_dropdown()
render_haircuts()
update_price()
