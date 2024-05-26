using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class MovementComp : MonoBehaviour
{
    [SerializeField] float movespeed = 1.0f;
    [SerializeField] Vector3 MoveDir ;
    Vector3 Destination;

    internal void SetMoveDir(Vector3 dir)
    {
        MoveDir = dir;
    }

    internal void SetMoveSpeed(float evnMoveSpeed)
    {
        movespeed = evnMoveSpeed;
    }

    public void SetDestination(Vector3 newDestination){
        Destination = newDestination;
    }

    // Start is called before the first frame update
    void Start()
    {
    }

    // Update is called once per frame
    void Update()
    {
        transform.position += MoveDir * Time.deltaTime * movespeed;
        if(Vector3.Dot(Destination - transform.position,MoveDir) < 0){
            Destroy(gameObject);
            //Debug.Log($"删除了{gameObject.name}");
        }
    }
}
