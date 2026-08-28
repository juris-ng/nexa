# NEXA NIA Phase 7 Test Script

Set-Location $PSScriptRoot

python -c "from nia_agent import NIAAgent; nia = NIAAgent(); print(nia.introduce()); print(); questions = ['What is happening in NEXA right now?', 'What happened at the warehouse?', 'Where is the mayor?', 'Tell me about the union.']; [print(f'USER: {question}\nNIA: {nia.chat(question)['response']}\n') for question in questions]; request = nia.create_action_request('investigate_location', {'location_id': 'eastern_warehouse'}, 'The audience requested an investigation into the labour dispute.'); print('CONTROLLED REQUEST CREATED:'); print(request); print(); print('PENDING REQUESTS:'); print(nia.get_pending_requests())"
