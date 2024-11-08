from flask import Flask, render_template, request, jsonify

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

    # Check if updating an existing event
    existing_event = next(
        (
            event
            for event in events
            if event["start"] == event_date and event["title"] == event_title
        ),
        None,
    )

    if existing_event:
        existing_event["description"] = event_description
        existing_event["todoList"] = todo_list
        message = f"Event '{event_title}' updated for {event_date}"
    else:
        new_event = {
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
    events = [event for event in events if event.get("id") != event_id]
    return jsonify({"message": "Event deleted successfully"})


if __name__ == "__main__":
    app.run(debug=True)
