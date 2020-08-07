function main(splash, args)
    assert(splash:go{
        splash.args.url,
        headers=splash.args.headers
    })
    assert(splash:wait(0.5))

    local entries = splash:history()
    local last_response = entries[#entries].response

    return {
        url = splash:url(),
        headers = last_response.headers,
        http_status = last_response.status,
        html = splash:html(),
    }
end