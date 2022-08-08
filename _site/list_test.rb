require 'yaml'
require 'test/unit'

class ListTest < Test::Unit::TestCase

  def test_list_structure
    assert File.exist?('list.yaml'), "There doesn't seem to be a `list.yaml` file present"
    assert Dir.exist?('things'), "There don't seem to be any Things"
  end

  def test_list_yaml
    list_yaml = YAML.load_file('list.yaml')
    required_yaml_keys = ["name", "description", "properties"]

    required_yaml_keys.each do |key|
      assert list_yaml.keys.include?(key), "`list.yaml` is missing #{key} property"
    end
  end

  def test_list_properties
    # Gather the List property keys defined in list.yaml
    list_yaml = YAML.load_file('list.yaml')
    property_keys = list_yaml['properties'].collect { |property| property['key'] }

    # Grab all the things
    thing_files = Dir.glob("things/*.yaml")

    # For each Thing file check that we're not defining invalid properties
    thing_files.each do |file|
      thing_name = File.basename(file)
      thing_yaml = YAML.load_file(file)
      thing_property_keys = thing_yaml.keys

      unassigned_thing_keys = thing_property_keys - property_keys
      assert unassigned_thing_keys.empty?, "#{thing_yaml} has invalid property keys #{unassigned_thing_keys.uniq}"

      unused_property_keys = property_keys - thing_property_keys
      warn "List has unused property keys #{unused_property_keys.uniq}" if !unused_property_keys.empty?
    end
  end

  def test_required_list_properties
    # Gather the List property keys defined in list.yaml
    list_yaml = YAML.load_file('list.yaml')
    required_properties = list_yaml['properties'].select { |property| property['key'] if property['required'] == "true" }

    # Grab all the things
    thing_files = Dir.glob("things/*.yaml")

    # For each Thing file check that we're not defining invalid properties
    thing_files.each do |file|
      thing_name = File.basename(file)
      thing_yaml = YAML.load_file(file)
      thing_property_keys = thing_yaml.keys

      required_properties.each do |property|
        assert thing_property_keys.include?(property['key']), "#{thing_name} is missing required property '#{property['key']}'"
      end
    end
  end
end
