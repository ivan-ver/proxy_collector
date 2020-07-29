function main(splash, args)
    assert(splash:go(args.url))
    assert(splash:wait(0.5))
    return {
        html = splash:html(),
        png = splash:png(),
        har = splash:har(),
    }
end