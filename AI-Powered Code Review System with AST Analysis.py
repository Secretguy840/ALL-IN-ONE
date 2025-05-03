import ast
import openai
from typing import List, Dict, Any
import hashlib
import difflib

class CodeReviewer:
    def __init__(self, openai_api_key: str):
        openai.api_key = openai_api_key
        self.cache: Dict[str, str] = {}
        
    def _get_code_hash(self, code: str) -> str:
        return hashlib.sha256(code.encode()).hexdigest()
    
    def _parse_ast(self, code: str) -> ast.Module:
        try:
            return ast.parse(code)
        except SyntaxError as e:
            raise ValueError(f"Syntax error in code: {e}")
    
    def _analyze_ast(self, node: ast.AST) -> List[Dict[str, Any]]:
        issues = []
        
        class Analyzer(ast.NodeVisitor):
            def visit_FunctionDef(self, node):
                # Check for long functions
                if len(node.body) > 30:
                    issues.append({
                        'type': 'complexity',
                        'message': f"Function '{node.name}' is too long ({len(node.body)} lines). Consider refactoring.",
                        'line': node.lineno,
                        'severity': 'warning'
                    })
                self.generic_visit(node)
            
            def visit_For(self, node):
                # Check for nested loops
                for child in ast.walk(node):
                    if isinstance(child, (ast.For, ast.While)):
                        issues.append({
                            'type': 'performance',
                            'message': "Nested loops detected. This may impact performance.",
                            'line': node.lineno,
                            'severity': 'warning'
                        })
                        break
                self.generic_visit(node)
        
        analyzer = Analyzer()
        analyzer.visit(node)
        return issues
    
    def _get_ai_feedback(self, code: str, context: str = "") -> str:
        cache_key = self._get_code_hash(code + context)
        if cache_key in self.cache:
            return self.cache[cache_key]
            
        prompt = f"""
        Analyze the following Python code and provide detailed feedback on:
        - Code quality and style
        - Potential bugs or edge cases
        - Security vulnerabilities
        - Performance optimizations
        - Best practices violations
        
        {context}
        
        Code:
        {code}
        
        Provide your feedback in markdown format with clear sections.
        """
        
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=1500
        )
        
        feedback = response.choices[0].message.content
        self.cache[cache_key] = feedback
        return feedback
    
    def review_code(self, code: str, previous_version: str = None, context: str = "") -> Dict[str, Any]:
        try:
            # AST Analysis
            tree = self._parse_ast(code)
            ast_issues = self._analyze_ast(tree)
            
            # AI Analysis
            ai_feedback = self._get_ai_feedback(code, context)
            
            # Diff analysis if previous version provided
            diff_analysis = None
            if previous_version:
                diff = difflib.unified_diff(
                    previous_version.splitlines(keepends=True),
                    code.splitlines(keepends=True),
                    fromfile='old.py',
                    tofile='new.py'
                )
                diff_analysis = ''.join(diff)
            
            return {
                'ast_issues': ast_issues,
                'ai_feedback': ai_feedback,
                'diff_analysis': diff_analysis,
                'metrics': {
                    'lines_of_code': len(code.splitlines()),
                    'functions': sum(1 for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)),
                    'classes': sum(1 for node in ast.walk(tree) if isinstance(node, ast.ClassDef))
                }
            }
        except Exception as e:
            return {
                'error': str(e),
                'ast_issues': [],
                'ai_feedback': "",
                'diff_analysis': None
            }
