from flask import Flask, render_template, request, jsonify

app = Flask("EventEaseCalendar")

# In-memory list to store events
events = []


# Route for the main calendar page
@app.route("/")
def home():
    # Pass events to the template to load them into the calendar
    return render_template("cal.html", events=events)


# Route to handle the event data sent from the modal form
@app.route("/add-event", methods=["POST"])
def add_event():
    data = request.json
    event_date = data.get("date")
    event_title = data.get("title")
    event_description = data.get("description")

    # Add the new event to the in-memory list
    new_event = {
        "title": event_title,
        "start": event_date,  # FullCalendar needs 'start' to define the event date
        "description": event_description,  # Extra data that can be used for tooltips, etc.
    }
    events.append(new_event)

    # Respond with a success message
    return jsonify(
        {"message": f"Event '{event_title}' added for {event_date}", "event": new_event}
    )


if __name__ == "__main__":
    app.run(debug=True)
