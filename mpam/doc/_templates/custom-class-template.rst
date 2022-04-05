{{ fullname | escape | underline}}

.. currentmodule:: {{ module }}

.. autoclass:: {{ objname }}

   {% set inherited_methods = [] %}
   {% set local_methods = [] %}
   {% for item in methods %}
       {% if item in inherited_members %}
           {{ inherited_methods.append(item) or "" }}
       {% else %}
           {{ local_methods.append(item) or "" }}
       {% endif %}
   {% endfor %}

   {% set inherited_attributes = [] %}
   {% set local_attributes = [] %}
   {% for item in attributes %}
       {% if item in inherited_members %}
           {{ inherited_attributes.append(item) or "" }}
       {% else %}
           {{ local_attributes.append(item) or "" }}
       {% endif %}
   {% endfor %}

   {% block attributes %}
   {% if local_attributes %}
   .. rubric:: {{ _('Attributes') }}

   .. autosummary::
   {% for item in local_attributes %}
      ~{{ name }}.{{ item }}
   {%- endfor %}
   {% endif %}
   {% endblock %}


   {% block inherited_attributes %}
   {% if inherited_attributes %}
   .. rubric:: {{ _('Inherited Attributes') }}

   .. autosummary::
   {% for item in inherited_attributes %}
      ~{{ name }}.{{ item }}
   {%- endfor %}
   {% endif %}
   {% endblock %}

   {% block methods %}
   {% if local_methods %}
   .. rubric:: {{ _('Methods') }}

   .. autosummary::
   {% for item in local_methods  %}
      ~{{ name }}.{{ item }}
   {%- endfor %}
   {% endif %}
   {% endblock %}
   

   {% block inherited_methods %}
   {% if inherited_methods %}
   .. rubric:: {{ _('Inherited Methods') }}

   .. autosummary::
   {% for item in inherited_methods %}
      ~{{ name }}.{{ item }}
   {%- endfor %}
   {% endif %}
   {% endblock %}
   