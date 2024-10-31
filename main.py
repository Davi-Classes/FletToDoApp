import flet as ft
from db import tasks, new_id
from typing import Callable


def Task(
    id: int, 
    name: str, 
    completed: bool, 
    on_change_status: Callable, 
    on_delete: Callable
) -> ft.Row:
    return ft.Row(
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[
            ft.Checkbox(
                label=name, 
                value=completed, 
                on_change=lambda e: on_change_status(id)
            ),
            ft.Row(
                spacing=0,
                controls=[
                    ft.IconButton(
                        content=ft.Icon(ft.icons.DELETE_OUTLINE, ft.colors.RED),
                        tooltip='Excluir',
                        on_click=lambda e: on_delete(id)
                    ),
                ]
            )
        ]
    )


def main(page: ft.Page):
    page.title = 'To Do APP'
    page.horizontal_alignment = ft.MainAxisAlignment.CENTER
    page.scroll = ft.ScrollMode.ADAPTIVE

    tasks_view = ft.Column(spacing=20)
    task_input = ft.TextField(hint_text="Insira uma tarefa...")

    def list_tasks():
        tasks_view.controls.clear()
        
        for task in tasks:
            task_control = Task(
                id=task.get('id'),
                name=task.get('name'), 
                completed=task.get('completed'),
                on_delete=delete_task_by_id,
                on_change_status=change_task_status_by_id,
            )

            tasks_view.controls.append(task_control)
        
        page.update()

    def create_new_task(e: ft.ControlEvent):
        new_task = {
            'id': new_id(),
            'name': task_input.value,
            'completed': False
        }
        tasks.append(new_task)
        task_control = Task(
            id=new_task.get('id'),
            name=new_task.get('name'), 
            completed=new_task.get('completed'),
            on_delete=delete_task_by_id,
            on_change_status=change_task_status_by_id,
        )

        tasks_view.controls.append(task_control)
        list_tasks()

    def delete_task_by_id(id: int):
        for i, task in enumerate(tasks):
            if task.get('id') == id:
                tasks.pop(i)
        
        list_tasks()

    def change_task_status_by_id(id: int):
        for i, task in enumerate(tasks):
            if task.get('id') == id:
                task['completed'] = not task['completed']

        list_tasks()

    list_tasks()

    page.add(
        ft.Column(
            width=600,
            controls=[
                ft.Row(
                    alignment=ft.alignment.center,
                    controls=[
                        ft.Text("Tarefas", theme_style=ft.TextThemeStyle.HEADLINE_MEDIUM)
                    ],
                ),
                ft.Row(
                    controls=[
                        task_input,
                        ft.FloatingActionButton(icon=ft.icons.ADD, on_click=create_new_task)
                    ]
                ),
                tasks_view
            ]
        )
    )


if __name__ == '__main__':
    ft.app(target=main)
