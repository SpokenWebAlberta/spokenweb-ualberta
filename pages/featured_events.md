---
layout: default
permalink: /featured_events
title: Featured Events
---

{% assign items = "" | split: "," %}

{% for temp in site.pages %}
    {% if temp.url contains "/events/" %}
        {% if temp.event_date %}
            {% assign items = items | push: temp %}
        {% endif %}
    {% endif %}
{% endfor %}

{% assign items = items | sort: "event_date" | reverse %}

{% assign final = "" | split: "," %}

{% for temp in items limit:3 %}
    {% assign final = final | push: temp.title %}
{% endfor %}

{% include featured_pages.html label="Event" items=final %}