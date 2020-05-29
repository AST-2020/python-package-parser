% Fakten

%father(peter, bernd).
%father(bernd, helmut).

%method(1, 2, '__init__', ['C', 'kernel']).
%method(3, 2, '__init2__', ['C', 'kernel']).
%class(2, 'SVC').

% Regeln

%grandfather(Person, Grandfather) :-
 %       father(Person, Father),
  %      father(Father, Grandfather).

%in_class(MethodId, ClassName) :-
 %       method(MethodId, ClassId, _, _),
  %      class(ClassId, ClassName).

% Anfragen
class(svcId,'C_SVC').
methode(initId,
        svcId
       ,'__init__'
   ['self',
   'C',
   'kernel',
   'degree',
   'gamma',
   'coef0',
   'shrinking',
   'probability',
   'tol',
   'cache_size',
   'class_weigh',
   'verbose',
   'max_iter',
   'decision_function_shape',
   'break_ties',
   'random_state']).

