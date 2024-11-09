from flask import Flask, render_template, request, jsonify
from uuid import uuid4

app = Flask("EventEaseCalendar")

# In-memory list to store events
events = []


# Route for the main calendar page
@app.route("/")
def home():
    return render_template("cal.html", events=events)


# Route to add or update an event
@app.route("/add-event", methods=["POST"])
def add_event():
    data = request.json
    event_date = data.get("date")
    event_title = data.get("title")
    event_description = data.get("description")
    todo_list = data.get("todoList", [])
    event_id = data.get("id")  # Get the ID from the request to find specific event

    # Check if updating an existing event by ID
    existing_event = next((event for event in events if event["id"] == event_id), None)

    if existing_event:
        # Update the existing event's title, description, and todo list
        existing_event["title"] = event_title
        existing_event["description"] = event_description
        existing_event["todoList"] = todo_list
        message = f"Event '{event_title}' updated for {event_date}"
    else:
        # Create a new event if none exists with the provided ID
        new_event = {
            "id": event_id or str(uuid4()),  # Ensure new events have unique IDs
            "title": event_title,
            "start": event_date,
            "description": event_description,
            "todoList": todo_list,
        }
        events.append(new_event)
        message = f"Event '{event_title}' added for {event_date}"

    return jsonify(
        {
            "message": message,
            "event": new_event if not existing_event else existing_event,
        }
    )


@app.route("/delete-event", methods=["POST"])
def delete_event():
    data = request.json
    event_id = data.get("id")
    global events
    events = [
        event for event in events if event["id"] != event_id
    ]  # Filter by unique ID
    return jsonify({"message": "Event deleted successfully"})


if __name__ == "__main__":
    app.run(debug=True)
