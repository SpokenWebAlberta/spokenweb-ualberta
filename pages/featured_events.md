---
layout: default
permalink: /featured_events/
title: 'Featured Events'
description: 'Explore SpokenWeb UAlberta's featured events.'
---

<h2>Latest Events</h2>

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

<hr class="network">

<h3>Network Wide Events </h3>

For more events hosted at institutes across the SpokenWeb Network, visit the [SpokenWeb Network Mainpage](https://spokenweb.ca/events/).