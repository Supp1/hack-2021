from app import app


@app.route('/<token>', methods=['POST'])
def handle(token):
    if token == bot.token:
        request_body_dict = request.json
        update = types.Update.de_json(request_body_dict)
        bot.process_new_updates([update])
        return app.response_class(
            response='OK',
            status=200,
            mimetype='core/json'
        )
    else:
        return app.response_class(
            response='Error',
            status=403,
            mimetype='core/json'
        )
