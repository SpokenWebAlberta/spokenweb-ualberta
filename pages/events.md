---
layout: default
permalink: /events/
title: All Events
---

<h2 class='page-title'>{{ page.title }}</h2>

<ul>
{% assign test = site.pages | sort: "event_date" %}
{% for temp in test %}
    {% if temp.event_date %}    
        {% if temp.url contains "/events/" %}
            <div>
                <img src="{{ temp.featured_image | absolute_url }}">
                <div>
                    <div>
                        <h2>{{ temp.subtitle }}</h2>
                        <h1>{{ temp.title }}</h1>
                        <p>{{ temp.description }}</p>
                        <h3 class='event-start'>
                            <time datetime='{{ temp.event_date | date_to_xmlschema }}'>
                              {{ temp.event_date | date: "%B %d" }}
                            </time>
                            {% if temp.event_end %}
                              <time datetime='{{ temp.publish_date | date_to_xmlschema }}'> -
                                  {{ temp.event_end | date: "%B %d, %Y" }}
                              </time>
                            {% endif %}
                          </h3>
                        <a href="{{ temp.url | relative_url }}" class="carousel-item__btn">Visit Event</a>
                    </div>
                </div>
            </div>
            <hr>
        {% endif %}
    {% endif %}
{% endfor %}
</ul>

