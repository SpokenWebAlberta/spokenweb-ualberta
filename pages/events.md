---
layout: default
permalink: /events/
title: All Events
---

<h2 class='page-title'>{{ page.title }}</h2>


{% assign items = "" | split: "," %}

{% for temp in site.pages %}
    {% if temp.url contains "/events/" %}
        {% if temp.event_date != nil %}
            {% assign items = items | push: temp %}
        {% endif %}
    {% endif %}
{% endfor %}

{% assign items = items | sort: "event_date" | reverse %}

<ul>
    {% for temp in items %}
    <div class='event-blog'>
        <div>
            <h2>{{ temp.subtitle }}</h2>
            <h1 class='event-title'>{{ temp.title }}</h1>
            <h3 class='event-start'>
                <time datetime='{{ temp.event_date | date_to_xmlschema }}'>
                    {{ temp.event_date | date: "%B %-d" }}
                </time>
                {% if temp.event_end %}
                    <time datetime='{{ temp.publish_date | date_to_xmlschema }}'> -
                        {{ temp.event_end | date: "%B %-d" }}
                    </time>
                {% endif %}
                <time datetime='{{ temp.event_date | date_to_xmlschema }}'>
                    {{ temp.event_date | date: ", %Y" }}
                </time>
            </h3>
        </div>
        <img src="{{ temp.featured_image | absolute_url }}">
        <p>{{ temp.description }}</p>
        <a href="{{ temp.url | relative_url }}" class="carousel-item__btn">Learn More</a>
    </div>
    <hr>
    {% endfor %}
</ul>

