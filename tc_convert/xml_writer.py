import traceback
from xml.dom import minidom
from tc_convert.common import TEST_SUITE, NAME, IMPORTANCE, TEST_TYPE, KEY_WORD, SUMMARY, PRECONDITIONS, STEP_NUMBER, \
    ACTIONS, EXPECTRESULTS, STEPS, STEP, TC_NAME, TC_STEPS, PRI_DICT
import os

def write_xml(ts_dict,modulename):
    xml_path=os.path.expanduser('~')+'/'+modulename+'.xml'
    dom = minidom.Document()
    root_node = dom.createElement(TEST_SUITE)
    root_node.setAttribute("name", modulename)
    dom.appendChild(root_node)
    for k1,v1 in ts_dict.items():
        module_node=dom.createElement(TEST_SUITE)
        module_node.setAttribute("name", k1)
        print('module_name is %s' % k1)
        for k, v in v1.items():

            testsuite_node = dom.createElement(TEST_SUITE)
            testsuite_node.setAttribute("name", k)

            for ele in v:
                if ele[PRECONDITIONS] is None or ele[IMPORTANCE] is None:
                    continue
                testcase_node = dom.createElement('testcase')
                testcase_node.setAttribute(NAME, ele['name'])

                importance_node = dom.createElement(IMPORTANCE)
                importance_node.appendChild(dom.createTextNode(PRI_DICT[ele[IMPORTANCE]]))

                pre_node = dom.createElement(PRECONDITIONS)
                pre_node.appendChild(dom.createTextNode(ele[PRECONDITIONS]))

                steps_node = dom.createElement(STEPS)

                for tc_step in ele['steps']:
                    step_node = dom.createElement(STEP)

                    step_number_node = dom.createElement(STEP_NUMBER)
                    step_text = dom.createTextNode(str(tc_step[STEP][STEP_NUMBER]))
                    step_number_node.appendChild(step_text)

                    action_node = dom.createElement(ACTIONS)
                    action_text = dom.createTextNode(tc_step[STEP][ACTIONS])
                    action_node.appendChild(action_text)

                    result_node = dom.createElement(EXPECTRESULTS)
                    result_text = dom.createTextNode(tc_step[STEP][EXPECTRESULTS])
                    result_node.appendChild(result_text)

                    step_node.appendChild(step_number_node)
                    step_node.appendChild(action_node)
                    step_node.appendChild(result_node)

                    steps_node.appendChild(step_node)

                testcase_node.appendChild(importance_node)
                testcase_node.appendChild(pre_node)
                testcase_node.appendChild(steps_node)
                testsuite_node.appendChild(testcase_node)
                if k is None:
                    module_node.appendChild(testcase_node)
            if k is not None:
                module_node.appendChild(testsuite_node)
        root_node.appendChild(module_node)


    try:
        with open(xml_path, 'w', encoding='UTF-8') as fh:
            # 4.writexml()第一个参数是目标文件对象，第二个参数是根节点的缩进格式，第三个参数是其他子节点的缩进格式，
            # 第四个参数制定了换行格式，第五个参数制定了xml内容的编码。
            dom.writexml(fh, indent='', addindent='\t', newl='\n', encoding='UTF-8')
        print('XML已生成到%s' % xml_path)
    except Exception as err:
        traceback.print_exc()
        print('错误信息：{0}'.format(err))