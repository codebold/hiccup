from dragonfly import (
    Grammar,
    AppContext,
    Rule,
    RuleRef,
    MappingRule,
    CompoundRule,
    Repetition,
    Alternative
)

from rules.choices.base import (
    _1to100
)


class GrammarBuilder(object):
    """
    Builder for dragonfly grammars.

    Provides the possibility to override commands.

    This class currently uses internal attributes of the grammar class and is only able to build grammars from mapping or special purpose rules.
    """
    def __init__(self, name, description=None, context=None, engine=None):
        self._grammar = Grammar(name, description, context, engine)

    def add_rule(self, rule):
        if not isinstance(rule, Rule):
            raise TypeError("Rule must be an instance of Rule!")
            
        self._grammar.add_rule(rule)
        return self

    def add_competitive_mapping_rule(self, base_rule, extension_rules):
        if not isinstance(base_rule, MappingRule):
            raise TypeError("Base rule must be an instance of MappingRule!")
        
        rules = list()
        base_context = base_rule._context
        
        for extension_rule in extension_rules:
            if not isinstance(extension_rule, MappingRule):
                raise TypeError("Extension rule must be an instance of MappingRule!")

            if not base_context:
                base_context = ~extension_rule._context
            else:
                base_context = base_context & ~extension_rule._context
            rules.append(self._combine_mapping_rules(base_rule._name + " (+" + extension_rule._name + ")", base_rule, extension_rule, extension_rule._context))

        base_rule._context = base_context
        rules.append(base_rule)

        for rule in rules:
            self._grammar.add_rule(rule)
        
        return self

    def _combine_mapping_rules(self, name, base_rule, extension_rule, context):
        mapping = base_rule._mapping.copy()
        mapping.update(extension_rule._mapping)
        extras_dict = base_rule._extras.copy()
        extras_dict.update(extension_rule._extras)
        extras = extras_dict.values()
        defaults = base_rule._defaults.copy()
        defaults.update(extension_rule._defaults)
        exported = base_rule._exported

        return MappingRule(name, mapping, extras, defaults, exported, context)

    def add_competitive_repeat_rule(self, base_rule, extension_rules):
        if not isinstance(base_rule, RepeatRuleComponents):
            raise TypeError("Base rule must be an instance of MappingRuleRepeatRuleComponents!")
        
        rules = list()
        base_context = base_rule.context
        
        for extension_rule in extension_rules:
            if not isinstance(extension_rule, RepeatRuleComponents):
                raise TypeError("Extension rule must be an instance of RepeatRuleComponents!")

            if not len(base_rule.rules) == len(extension_rule.rules):
                raise ValueError("Not every rule has an extension rule!")

            if not base_context:
                base_context = ~extension_rule._context
            else:
                base_context = base_context & ~extension_rule._context
            rules.append(self._combine_repeat_rules(extension_rule._name, base_rule, extension_rule, extension_rule.context))

        base_rule._context = base_context
        rules.append(RepeatRule(base_rule.name, base_rule.context, base_rule.rules))

        for rule in rules:
            self._grammar.add_rule(rule)
        
        return self

    def _combine_repeat_rules(self, name, base_rules, extension_rules, context):
        rules = list()
        
        for i in range(len(base_rules.rules)):
            if extension_rules.rules[i]:
                rules.append(self._combine_mapping_rules(base_rules.rules[i]._name + " (+" + extension_rules.rules[i]._name + ") [" + str(context)+ "]", base_rules.rules[i], extension_rules.rules[i], None))
            else:
                rules.append(base_rules.rules[i])

        return RepeatRule(name, context, rules)

    def build(self):
        return self._grammar



class RepeatRuleComponents(object):
    """
        The components required for building a repeat rule.
    """

    def __init__(self, name, context, rules):
        self._name = name
        self._context = context
        self._rules = rules

    name = property(lambda self: self._name, doc="The name of this repeat rule. (Read-only)")
    context = property(lambda self: self._context, doc="The context in which this repeat rule will be active. (Read-only)")
    rules = property(lambda self: self._rules, doc="The rules this repeat rule consists of. (Read-only)")
        
        


class RepeatRule(CompoundRule):
    """
    Rule that allows the repetetive execution of commands from the referenced rule set.
    """
    spec = "[<1to100>] <sequence> [then]"
    extras = [_1to100]
    defaults = {"1to100": 1}

    def __init__(self, name, context, rules):
        self._name = name
        
        rule_refs = list()
        
        for rule_ in rules:
            rule_refs.append(RuleRef(rule=rule_))

        # max should not be greater than 7
        self.extras.append(Repetition(Alternative(rule_refs), min=1, max=6, name="sequence"))

        super(RepeatRule, self).__init__(context=context)

    def _process_recognition(self, node, extras):
        sequence = extras["sequence"]
        count = extras["1to100"]
        for i in range(count):
            for action in sequence:
                action.execute()
