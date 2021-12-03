from core.label_config import parse_config


def test_parsing_label_config():
    """
    Test frames extraction with disabled in the end and frame count > disabled key frame
    """
    label_config = '''
            <View><Text name="meta_info" value="$meta_info"></Text>
              <Text name="text" value=" $text "></Text>
              <Choices name="text_class" choice="single" toName="text">
                <Choice value="class_A"></Choice>
                <Choice value="class_B"></Choice>
              </Choices>
            </View>'''
    config = parse_config(label_config)
    assert 'text_class' in config
    assert config['text_class']['type'] == 'Choices'
    assert config['text_class']['to_name'] == ['text']
    assert config['text_class']['labels'] == ['class_A', 'class_B']