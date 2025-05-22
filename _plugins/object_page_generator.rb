module ObjectGenerator
  class ObjectPageGenerator < Jekyll::Generator
    safe true

    def generate(site)
      site.data["objects"].each do | object_id, data |
        site.pages << ObjectPage.new(site, object_id)
      end
    end
  end

  # Subclass of `Jekyll::Page` with custom method definitions.
  class ObjectPage < Jekyll::Page
    def initialize(site, object_id)
      @site = site             # the current site instance.
      @base = site.source      # path to the source directory.
      @dir  = "objects"         # the directory the page will reside in.

      # All pages have the same filename, so define attributes straight away.
      @basename = "#{object_id}"      # filename without the extension.
      @ext      = '.md'      # the extension.
      @name     = "#{object_id}.md" # basically @basename + @ext.

      object_data = site.data["objects"][object_id]

      # Initialize data hash with a key pointing to all posts under current category.
      # This allows accessing the list in a template via `page.linked_docs`.
      @data = {
        'iden' => object_id,
        'title' => object_data["title"],
        'description' => object_data["description"],
      }

      # Look up front matter defaults scoped to type `categories`, if given key
      # doesn't exist in the `data` hash.
      data.default_proc = proc do |_, key|
        site.frontmatter_defaults.find(relative_path, :objects, key)
      end
    end
  end
end
