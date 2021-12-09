from label_studio_tools.postprocessing.video import extract_key_frames

def test_video_disabled_till_end():
    """
    Test frames extraction with disabled in the end and frame count > disabled key frame
    """
    example = [
        {
            "id": "tJhYZLMC9G",
            "type": "videorectangle",
            "value": {
                "labels": [
                    "Airplane"
                ],
                "frameCount": 10000000,
                "sequence": [
                    {
                        "frame": 1,
                        "enabled": True,
                        "x": 38,
                        "y": 38,
                        "width": 41,
                        "height": 22,
                        "rotation": 0
                    },
                    {
                        "frame": 5,
                        "enabled": False,
                        "x": 40,
                        "y": 49,
                        "width": 56,
                        "height": 34,
                        "rotation": 30
                    }
                ],
                "from_name": "test"
            }
        }
    ]
    key_frames = extract_key_frames(example)
    assert len(key_frames[0]['value']['sequence']) == 5
    key_frames = key_frames[0]['value']['sequence']
    assert key_frames[0]['x'] == 38
    assert key_frames[0]['y'] == 38
    assert key_frames[0]['width'] == 41
    assert key_frames[0]['height'] == 22
    assert key_frames[0]['rotation'] == 0
    assert key_frames[4]['x'] == 40
    assert key_frames[4]['y'] == 49
    assert key_frames[4]['width'] == 56
    assert key_frames[4]['height'] == 34
    assert key_frames[4]['rotation'] == 30
    assert key_frames[2]['x'] == 39
    assert key_frames[2]['y'] == 43.5
    assert key_frames[2]['width'] == 48.5
    assert key_frames[2]['height'] == 28
    assert key_frames[2]['rotation'] == 15
    assert key_frames[2]['auto']
    assert not key_frames[0].get('auto')
    assert not key_frames[4].get('auto')


def test_video_enabled_till_end():
    """
    Test frames extraction with enabled in the end and frame count > enabled key frame
    """
    example = [
        {
            "id": "tJhYZLMC9G",
            "type": "videorectangle",
            "value": {
                "labels": [
                    "Airplane"
                ],
                "frameCount": 10,
                "sequence": [
                    {
                        "frame": 1,
                        "enabled": True,
                        "x": 38,
                        "y": 38,
                        "width": 41,
                        "height": 22,
                        "rotation": 0
                    },
                    {
                        "frame": 5,
                        "enabled": True,
                        "x": 40,
                        "y": 49,
                        "width": 41,
                        "height": 22,
                        "rotation": 0
                    }
                ]
            }
        }
    ]
    key_frames = extract_key_frames(example)[0]['value']['sequence']
    assert len(key_frames) == 10
    assert key_frames[0]['x'] == 38
    assert key_frames[0]['y'] == 38
    assert key_frames[0]['width'] == 41
    assert key_frames[0]['height'] == 22
    assert key_frames[0]['rotation'] == 0
    assert key_frames[4]['x'] == 40
    assert key_frames[4]['y'] == 49
    assert key_frames[4]['width'] == 41
    assert key_frames[4]['height'] == 22
    assert key_frames[4]['rotation'] == 0
    assert key_frames[2]['x'] == 39
    assert key_frames[2]['y'] == 43.5
    assert key_frames[2]['width'] == 41
    assert key_frames[2]['height'] == 22
    assert key_frames[2]['rotation'] == 0
    assert key_frames[2]['auto']
    assert not key_frames[0].get('auto')
    assert not key_frames[4].get('auto')
    assert key_frames[5]['x'] == 40
    assert key_frames[5]['y'] == 49
    assert key_frames[5]['width'] == 41
    assert key_frames[5]['height'] == 22
    assert key_frames[5]['rotation'] == 0
    assert key_frames[8]['x'] == 40
    assert key_frames[8]['y'] == 49
    assert key_frames[8]['width'] == 41
    assert key_frames[8]['height'] == 22
    assert key_frames[8]['rotation'] == 0
    assert key_frames[9]['x'] == 40
    assert key_frames[9]['y'] == 49
    assert key_frames[9]['width'] == 41
    assert key_frames[9]['height'] == 22
    assert key_frames[9]['rotation'] == 0
    assert key_frames[8]['auto']
    assert key_frames[5].get('auto')
    assert key_frames[9].get('auto')


def test_video_enabled_till_end_one_frame():
    """
    Test frames extraction with enabled in the end and frame count > enabled key frame
    """
    example = [
        {
            "id": "tJhYZLMC9G",
            "type": "videorectangle",
            "value": {
                "labels": [
                    "Airplane",
                    "Test"
                ],
                "frameCount": 10,
                "sequence": [
                    {
                        "frame": 1,
                        "enabled": True,
                        "x": 38,
                        "y": 38,
                        "width": 41,
                        "height": 22,
                        "rotation": 0
                    }
                ]
            }
        }
    ]
    key_frames = extract_key_frames(example)[0]['value']['sequence']
    print(key_frames)
    assert len(key_frames) == 10
    assert key_frames[0]['x'] == 38
    assert key_frames[0]['y'] == 38
    assert key_frames[0]['width'] == 41
    assert key_frames[0]['height'] == 22
    assert key_frames[0]['rotation'] == 0
    assert key_frames[9]['x'] == 38
    assert key_frames[9]['y'] == 38
    assert key_frames[9]['width'] == 41
    assert key_frames[9]['height'] == 22
    assert key_frames[9]['rotation'] == 0


def test_video_disabled_till_end_one_frame():
    """
    Test frames extraction with disabled in the end and frame count > enabled key frame
    """
    example = [
        {
            "id": "tJhYZLMC9G",
            "type": "videorectangle",
            "value": {
                "labels": [
                    "Airplane"
                ],
                "frameCount": 10,
                "sequence": [
                    {
                        "frame": 1,
                        "enabled": False,
                        "x": 38,
                        "y": 38,
                        "width": 41,
                        "height": 22,
                        "rotation": 0
                    }
                ]
            }
        }
    ]
    key_frames = extract_key_frames(example)[0]['value']['sequence']
    print(key_frames)
    assert len(key_frames) == 0


def test_video_disabled_till_end_keyframe_count():
    """
    Test frames extraction with disabled in the end and frame count > disabled key frame
    """
    example = [
        {
            "id": "tJhYZLMC9G",
            "type": "videorectangle",
            "value": {
                "labels": [
                    "Airplane"
                ],
                "frameCount": 10000000,
                "sequence": [
                    {
                        "frame": 1,
                        "enabled": True,
                        "x": 38,
                        "y": 38,
                        "width": 41,
                        "height": 22,
                        "rotation": 0
                    },
                    {
                        "frame": 5,
                        "enabled": False,
                        "x": 40,
                        "y": 49,
                        "width": 41,
                        "height": 22,
                        "rotation": 0
                    },
                    {
                        "frame": 11,
                        "enabled": True,
                        "x": 38,
                        "y": 38,
                        "width": 41,
                        "height": 22,
                        "rotation": 0
                    },
                    {
                        "frame": 15,
                        "enabled": False,
                        "x": 40,
                        "y": 49,
                        "width": 41,
                        "height": 22,
                        "rotation": 0
                    }
                ]
            }
        }
    ]
    key_frames = extract_key_frames(example)[0]['value']['sequence']
    assert len(key_frames) == 10
    assert key_frames[5]['x'] == 38
    assert key_frames[5]['y'] == 38
    assert key_frames[5]['width'] == 41
    assert key_frames[5]['height'] == 22
    assert key_frames[5]['rotation'] == 0
    assert key_frames[9]['x'] == 40
    assert key_frames[9]['y'] == 49
    assert key_frames[9]['width'] == 41
    assert key_frames[9]['height'] == 22
    assert key_frames[9]['rotation'] == 0
    assert key_frames[7]['x'] == 39
    assert key_frames[7]['y'] == 43.5
    assert key_frames[7]['width'] == 41
    assert key_frames[7]['height'] == 22
    assert key_frames[7]['rotation'] == 0


def test_no_label_result():
    """
    Test frames extraction with no label and disabled in the end and frame count > disabled key frame
    """
    example = [
        {
            "id": "tJhYZLMC9G",
            "type": "videorectangle",
            "value": {
                "frameCount": 10000000,
                "sequence": [
                    {
                        "frame": 1,
                        "enabled": True,
                        "x": 38,
                        "y": 38,
                        "width": 41,
                        "height": 22,
                        "rotation": 0
                    },
                    {
                        "frame": 5,
                        "enabled": False,
                        "x": 40,
                        "y": 49,
                        "width": 41,
                        "height": 22,
                        "rotation": 0
                    },
                    {
                        "frame": 11,
                        "enabled": True,
                        "x": 38,
                        "y": 38,
                        "width": 41,
                        "height": 22,
                        "rotation": 0
                    },
                    {
                        "frame": 15,
                        "enabled": False,
                        "x": 40,
                        "y": 49,
                        "width": 41,
                        "height": 22,
                        "rotation": 0
                    }
                ]
            }
        }
    ]
    key_frames = extract_key_frames(example)[0]['value']['sequence']
    assert len(key_frames) == 10
    assert key_frames[5]['x'] == 38
    assert key_frames[5]['y'] == 38
    assert key_frames[5]['width'] == 41
    assert key_frames[5]['height'] == 22
    assert key_frames[5]['rotation'] == 0
    assert key_frames[9]['x'] == 40
    assert key_frames[9]['y'] == 49
    assert key_frames[9]['width'] == 41
    assert key_frames[9]['height'] == 22
    assert key_frames[9]['rotation'] == 0
    assert key_frames[7]['x'] == 39
    assert key_frames[7]['y'] == 43.5
    assert key_frames[7]['width'] == 41
    assert key_frames[7]['height'] == 22
    assert key_frames[7]['rotation'] == 0